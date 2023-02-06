#!/usr/bin/env python3

import errno
import io
import re
import sys

from .db import Connection, Cursor

def get_code_range(fragment):
    if '-' in fragment:
        m = re.match('([0-9A-Fa-f]+)-([0-9A-Fa-f]+)', fragment)
        min = int(m.group(1), 16)
        max = int(m.group(2), 16)
        r = (min, max)
    else:
        m = re.match('[0-9A-Fa-f]+', fragment)
        r = int(fragment, 16)
    return r

def search(fragment, by, short=False, utf8=False):
    with Connection() as conn:
        char_list = []
        if by == 'code':
            code_range = get_code_range(fragment)
            if type(code_range) is tuple:
                cond = f'where cp.code >= {code_range[0]} and cp.code <= {code_range[1]}'
            else:
                cond = f'where cp.code = {code_range}'
            dml = f'select char.id, char.codetext, char.name, char.char from char inner join codepoint as cp on char.id = cp.char {cond} order by char.char'
            with Cursor(conn) as cur:
                cur.execute(dml)
                char_list = cur.fetchall()
        elif by == 'block':
            dml = f'select char.id, char.codetext, char.name, char.char from char where block like "%{fragment}%" order by char.char'
            with Cursor(conn) as cur:
                cur.execute(dml)
                char_list = cur.fetchall()
        else:
            dml = f'select id, codetext, name, char from char where name like "%{fragment}%" order by char'
            with Cursor(conn) as cur:
                cur.execute(dml)
                char_list = cur.fetchall()

        for (id, codetext, name, char) in char_list:
            if utf8:
                codetext = ' '.join(f'{u:X}' for u in [int.from_bytes(chr(int(c, 16)).encode(), 'big') for c in codetext.split(' ')])

            if short:
                print(f'{char}', end='')
            else:
                print(f'{char} {codetext} {name}')

def ucsearch():
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8")
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", line_buffering=True)
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", line_buffering=True)

    import argparse
    parser = argparse.ArgumentParser(description='Search unicode characters')
    parser.add_argument('expression', nargs='+', metavar='EXPR', help='expression to search')
    group_by = parser.add_mutually_exclusive_group()
    group_by.add_argument('-b', '--block', action='store_const', dest='by', const='block', help='by block name')
    group_by.add_argument('-c', '--code', action='store_const', dest='by', const='code', help='by code')
    parser.add_argument('-s', '--short', action='store_true', help='print character only')
    parser.add_argument('-u', '--utf8', action='store_true', help='print utf8')

    args = parser.parse_args()

    if args.by:
        by = args.by
    else:
        by = None

    for expr in args.expression:
        search(expr, by, short=args.short, utf8=args.utf8)

    return 0