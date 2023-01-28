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

def get_cp(char):
    cp = char.attrib.get('cp')
    first_cp = char.attrib.get('first-cp')
    last_cp = char.attrib.get('last-cp')
    value = ''
    if cp:
        value = cp
    elif first_cp or last_cp:
        if first_cp:
            value = value + first_cp
        value = value + '-'
        if last_cp:
            value = value + last_cp
    return value.upper()

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

    with Connection() as conn:
        with Cursor(conn) as cur:
            count = 0
            for char in repertoire:
                cp = get_cp(char)

                if char.tag != tag_char:
                    if char.tag == tag_reserved:
                        print(f'Found reserved code(s): {cp}', file=sys.stderr)
                    elif char.tag == tag_noncharacter:
                        print(f'Found non character code(s): {cp}', file=sys.stderr)
                    elif char.tag == tag_surrogate:
                        print(f'Found surrogate code(s): {cp}', file=sys.stderr)
                    else:
                        print(f'Found miscellaneous {char.tag}', file=sys.stderr)
                    continue

                name = get_name(char)
                if not name:
                    print(f'Found no character(s): {cp}', file=sys.stderr)
                    continue
                try:
                    if int(cp, 16) == 0:
                        char = None
                    else:
                        char = chr(int(cp, 16))
                except ValueError as e:
                    print(f'Invalid character(s) {cp} ({name})', file=sys.stderr)
                    continue

                if len(cp) > 0:
                        value_code = f'"{cp}"'
                        value_name = f'"{name}"'
                        if char:
                            escaped_char = str(char).replace('"', '""')
                            value_char = f'"{escaped_char}"'
                        else:
                            value_char = 'NULL'
                        dml = f'insert into char(code, name, char) values({value_code}, {value_name}, {value_char})'
                        cur.execute(dml)
                        count = count + 1

            conn.commit()
            print(f'Stored {count} characters', file=sys.stderr)

    return count

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