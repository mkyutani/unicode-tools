#!/usr/bin/env python3

import errno
import io
import sys

from .db import Connection, Cursor

def search(fragment, by_code=False, short=False):
    with Connection() as conn:
        with Cursor(conn) as cur:
            if by_code:
                cond = f'where code = "{fragment.upper()}"'
            else:
                cond = f'where name like "%{fragment.upper()}%"'
            dml = f'select * from char {cond}'
            cur.execute(dml)
            for (code, name, char) in cur.fetchall():
                if short:
                    print(f'{char}', end='')
                else:
                    print(f'{char} {code} {name}')

def ucsearch():
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8")
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", line_buffering=True)
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", line_buffering=True)

    import argparse
    parser = argparse.ArgumentParser(description='Search unicode characters')
    parser.add_argument('expression', nargs='+', metavar='EXPR', help='expression to search')
    parser.add_argument('-c', '--code', action='store_true', help='by code')
    parser.add_argument('-s', '--short', action='store_true', help='print character only')
    parser.add_argument('-I', '--info', nargs=1, default=[None], help='print character information')

    if len(sys.argv) < 2:
        print(parser.format_usage(), file=sys.stderr)
        exit(errno.EPERM)

    args = parser.parse_args()

    for expr in args.expression:
        search(expr, by_code=args.code, short=args.short)

    return 0