#!/usr/bin/env python3

import io
import os
import requests
import sys
import tempfile
import zipfile
import xml.etree.ElementTree as et

from .db import Database, Connection, Cursor

unicode_zip_url = 'https://www.unicode.org/Public/15.0.0/ucdxml/ucd.all.flat.zip'
unicode_zip_filename = 'ucd.all.flat.zip'
unicode_xml_filename = 'ucd.all.flat.xml'

namespace = '{http://www.unicode.org/ns/2003/ucd/1.0}'
tag_ucd = namespace + 'ucd'
tag_description = namespace + 'description'
tag_repertoire = namespace + 'repertoire'
tag_char = namespace + 'char'
tag_noncharacter = namespace + 'noncharacter'
tag_reserved = namespace + 'reserved'
tag_surrogate = namespace + 'surrogate'
tag_name_alias = namespace + 'name-alias'
tag_blocks = namespace + 'blocks'
tag_block = namespace + 'block'

def get():
    zip_filepath = '(Not assigned)'

    try:
        with tempfile.TemporaryDirectory() as tmpdir:

            zip_filepath = os.path.join(tmpdir, unicode_zip_filename)

            print(f'Downloading {unicode_zip_url} ...', file=sys.stderr)

            res = requests.get(unicode_zip_url, stream=True)
            if res.status_code >= 400:
                print(f'Fetch error: {res.status_code}', file=sys.stderr)
                return None

            content_type = res.headers['Content-Type']
            if content_type != 'application/zip':
                print(f'Invalid content type: {content_type}')
                return None

            with open(zip_filepath, 'wb') as fzip:
                for chunk in res.iter_content(chunk_size=1024):
                    if chunk:
                        fzip.write(chunk)
                        fzip.flush()

            print(f'Downloaded {zip_filepath}', file=sys.stderr)

            with zipfile.ZipFile(zip_filepath, 'r') as zip:
                xml_list = zip.read(unicode_xml_filename)

            print('Extracted unicode data xml', file=sys.stderr)

            return xml_list

    except Exception as e:
        print(f'Failed to store zip from {unicode_zip_url} to {zip_filepath}', file=sys.stderr)
        print(f'{type(e).__name__}: {str(e)}', file=sys.stderr)
        return None

def get_cp(tag):
    cp = tag.attrib.get('cp')
    first_cp = tag.attrib.get('first-cp')
    last_cp = tag.attrib.get('last-cp')

    if cp:
        first_cp = cp
        last_cp = cp

    if not (first_cp and last_cp):
        print(f'Invalid code range: cp={cp}, first_cp={first_cp}, last_cp={last_cp}', file=sys.stderr)
        return None

    min = int(first_cp, 16)
    max = int(last_cp, 16)

    return (min, max)

def get_char_cp(char):

    value = None
    r = get_cp(char)
    if r:
        min = r[0]
        max = r[1]
        if char.tag != tag_char:
            if min == max:
                code_range = f'{min:X}'
            else:
                code_range = f'{min:X}-{max:X}'
            code_range = code_range.upper()

            if char.tag == tag_reserved:
                print(f'Found reserved code(s): {code_range}', file=sys.stderr)
            elif char.tag == tag_noncharacter:
                print(f'Found non character code(s): {code_range}', file=sys.stderr)
            elif char.tag == tag_surrogate:
                print(f'Found surrogate code(s): {code_range}', file=sys.stderr)
            else:
                print(f'Found unknown tag: {char.tag} {code_range}', file=sys.stderr)
            return []
            
        value = range(min, max + 1)
        return value

def get_name(char):
    value = []
    name = char.attrib.get('na')
    name1 = char.attrib.get('na1')
    if name and len(name) > 0:
        value.append(name.upper())
    if name1 and len(name1) > 0 and name != name1:
        value.append(name1.upper())
    for alias in char:
        if alias.tag == tag_name_alias:
            alias_name = alias.attrib.get('alias')
            if alias_name and len(alias_name) > 0 and alias_name not in value:
                value.append(alias_name.upper())
    return '; '.join(value)

def store(xml_list):
    if not xml_list:
        return None

    root = et.parse(io.BytesIO(xml_list)).getroot()
    if root.tag != tag_ucd:
        print(f'Unexpected XML scheme: {root.tag}', file=sys.stderr)
        return None

    description = root.find(tag_description)
    repertoire = root.find(tag_repertoire)
    blocks = root.find(tag_blocks)

    with Connection() as conn:
        with Cursor(conn) as cur:
            count = 0
            for char in repertoire:
                code_range = get_char_cp(char)
                for code in code_range:
                    value_code = code
                    name = get_name(char)
                    if not name:
                        print(f'Found no character: {code:X}', file=sys.stderr)
                        continue
                    value_name = f'"{name}"'

                    try:
                        if code == 0:
                            value_char = 'NULL'
                        else:
                            escaped_char = str(chr(code)).replace('"', '""')
                            value_char = f'"{escaped_char}"'
                    except ValueError as e:
                        print(f'Invalid character {code:X} ({name})', file=sys.stderr)
                        continue

                    dml = f'insert into char(code, name, char) values({value_code}, {value_name}, {value_char})'
                    cur.execute(dml)
                    count = count + 1

            conn.commit()
            print(f'Stored {count} characters', file=sys.stderr)

        with Cursor(conn) as cur:
            count = 0
            for block in blocks:
                r = get_cp(block)
                if not r:
                    continue

                min = r[0]
                max = r[1]
                name = block.attrib.get('name')
                if not name:
                    print(f'No name found in block: {min:X}-{max:X}', file=sys.stderr)
                    continue

                escaped_name = name.replace('"', '""')
                value_name = f'"{escaped_name}"'

                dml = f'insert into block(name, first, last) values({value_name}, {min}, {max})'
                print(dml)
                cur.execute(dml)
                count = count + 1

            conn.commit()
            print(f'Stored {count} blocks', file=sys.stderr)

def wrap_io():
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8")
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", line_buffering=True)
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", line_buffering=True)

def uccreatedatabase():
    wrap_io()
    Database().create()
    store(get())
    return 0

def ucdeletedatabase():
    wrap_io()
    Database().delete()
    return 0