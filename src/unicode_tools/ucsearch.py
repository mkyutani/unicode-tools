#!/usr/bin/env python3

import errno
import io
import json
import os
import re
import sys
import zipfile

unicode_database_filename = 'unicode_database.json'
unicode_database_path = os.path.abspath(os.path.join(os.path.dirname(__file__), f'../../../../share/applications/{unicode_database_filename}'))
unicode_database_zip_path = unicode_database_path + '.zip'

def search(fragment, unicode_database):
    if not unicode_database:
        return None
    if not fragment:
        return None

    for u in unicode_database['chars']:
        name = u['n']
        code = u['cd']
        char = u['c']
        if re.search(fragment, u['cd'], flags=re.IGNORECASE) or re.search(fragment, u['n'], flags=re.IGNORECASE):
            print(f'{char} {code} {name}')

def load():
    try:

        if os.path.exists(unicode_database_path):
            with open(unicode_database_path, 'r') as fin:
                return json.load(fin)
        elif os.path.exists(unicode_database_zip_path):
            with zipfile.ZipFile(unicode_database_zip_path, 'r') as zip:
                json_data = zip.read(unicode_database_filename)
                return json.loads(json_data)

    except Exception as e:
        print(f'Failed to load unicode database: {unicode_database_path}', file=sys.stderr)
        print(f'{type(e).__name__}: {str(e)}', file=sys.stderr)
        return None

def ucsearch():
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8")
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", line_buffering=True)
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", line_buffering=True)

    import argparse
    parser = argparse.ArgumentParser(description='Search unicode characters')
    parser.add_argument('expression', nargs='+', metavar='EXPR', help='expression to search')
    parser.add_argument('-I', '--info', nargs=1, default=[None], help='print character information')

    if len(sys.argv) < 2:
        print(parser.format_usage(), file=sys.stderr)
        exit(errno.EPERM)

    args = parser.parse_args()

    unicode_database = load()
    if not unicode_database:
        return errno.EIO

    for expr in args.expression:
        search(expr, unicode_database)

    return 0