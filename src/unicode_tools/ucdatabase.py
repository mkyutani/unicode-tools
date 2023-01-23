#!/usr/bin/env python3

import io
import json
import os
import re
import requests
import sys
import tempfile
import zipfile
import xml.etree.ElementTree as et

unicode_zip_url = 'https://www.unicode.org/Public/15.0.0/ucdxml/ucd.all.flat.zip'
unicode_zip_filename = 'ucd.all.flat.zip'
unicode_xml_filename = 'ucd.all.flat.xml'
unicode_database_filename = 'unicode_database.json'
unicode_database_path = os.path.abspath(os.path.join(os.path.dirname(__file__), f'../../../../share/applications/{unicode_database_filename}'))
unicode_database_zip_path = unicode_database_path + '.zip'

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

def analyze(xml_list):
    if not xml_list:
        return None

    unicode_set = {}

    root = et.parse(io.BytesIO(xml_list)).getroot()
    if root.tag != tag_ucd:
        print(f'Unexpected XML scheme: {root.tag}', file=sys.stderr)
        return None

    description = root.find(tag_description)
    repertoire = root.find(tag_repertoire)
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
            char = chr(int(cp, 16))
        except ValueError as e:
            print(f'Invalid character(s) {cp} ({name})', file=sys.stderr)
            continue

        if len(cp) > 0:
            unicode_set.update({
                cp: {
                    'name': name,
                    'code': cp,
                    'char': char
                }
            })

    unicode_database = []
    
    for u in unicode_set:
        unicode_database.append(
            {
                'cd': unicode_set[u]['code'],
                'n': unicode_set[u]['name'],
                'c': unicode_set[u]['char']
            }
        )

    print('Analyzed unicode zip successfully', file=sys.stderr)

    return unicode_database

def save(unicode_database):
    if not unicode_database:
        return

    with open(unicode_database_path, 'w') as fout:
        json_out = {
            'chars': unicode_database
        }
        json.dump(json_out, fout, indent=1)

    print(f'Created json database: {unicode_database_path}', file=sys.stderr)

def delete():
    if os.path.exists(unicode_databasae_zip_path):
        os.remove(unicode_database_zip_path)
        print(f'Deleted json database zip: {unicode_database_zip_path}', file=sys.stderr)
    if os.path.exists(unicode_database_path):
        os.remove(unicode_database_path)
        print(f'Deleted json database: {unicode_database_path}', file=sys.stderr)

def zip():
    try:
        with zipfile.ZipFile(unicode_database_zip_path, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zip:
            zip.write(unicode_database_path, arcname=unicode_database_filename)
            print(f'Archived unicode database: {unicode_database_zip_path}', file=sys.stderr)

        os.remove(unicode_database_path)

    except Exception as e:
        print(f'Failed to archive unicode database {unicode_database_path}', file=sys.stderr)
        print(f'{type(e).__name__}: {str(e)}', file=sys.stderr)

def uccreatedatabase():
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8")
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", line_buffering=True)
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", line_buffering=True)

    import argparse
    parser = argparse.ArgumentParser(description='Create database for unicode tool')
    parser.add_argument('-z', '--zip', action='store_true', help='zip database')

    args = parser.parse_args()

    save(analyze(get()))

    if args.zip:
        zip()

    return 0

def ucdeletedatabase():
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8")
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", line_buffering=True)
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", line_buffering=True)
    delete()
    return 0