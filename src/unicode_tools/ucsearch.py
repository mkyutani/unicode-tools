#!/usr/bin/env python3

import errno
import io
import json
import os
import re
import sys

unicode_database_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../share/applications/unicode_database.json'))

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
    with open(unicode_database_path, 'r') as fin:
        return json.load(fin)

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

if __name__ == '__main__':
    exit(ucsearch())