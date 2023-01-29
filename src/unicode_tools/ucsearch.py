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

def search_codes(fragment, by, short=False):
    with Connection() as conn:
        char_list = []
        if by == 'code':
            code_range = get_code_range(fragment)
            if type(code_range) is tuple:
                cond = f'where code >= {code_range[0]} and code <= {code_range[1]}'
            else:
                cond = f'where code = {code_range}'
            dml = f'select * from char {cond}'
            with Cursor(conn) as cur:
                cur.execute(dml)
                char_list = cur.fetchall()
        elif by == 'block':
            dml_block = f'select * from block where name like "%{fragment}%"'
            with Cursor(conn) as cur_block:
                cur_block.execute(dml_block)
                block_list = cur_block.fetchall()
            for (block_name, min, max) in block_list:
                dml = f'select * from char where code >= {min} and code <= {max}'
                with Cursor(conn) as cur:
                    cur.execute(dml)
                    char_list.extend(cur.fetchall())
        else:
            dml = f'select * from char where name like "%{fragment}%" order by code'
            with Cursor(conn) as cur:
                cur.execute(dml)
                char_list = cur.fetchall()

        char_list.sort(key=lambda x: x[0])
        for (code, name, char) in char_list:
            if short:
                print(f'{char}', end='')
            else:
                print(f'{char} {code:X} {name}')

def search_flags(regional_code, short=False):
    flag = ''
    name = ''
    codes = []
    for c in (regional_code.upper())[0:2]:
        code = 0x1f1e5 + (ord(c) - ord('@'))
        flag = flag + chr(code)
        codes.append(f'{code:X}')
        name = name + c
    if short:
        print(f'{flag}')
    else:
        code_value = '+'.join(codes)
        print(f'{flag} {code_value} FLAG OF {name}')

def search(expr, by, short):
    if by == 'flag':
        search_flags(expr, short)
    else:
        search_codes(expr, by, short)

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
    group_by.add_argument('-f', '--flag', action='store_const', dest='by', const='flag', help='search regional flags')
    parser.add_argument('-s', '--short', action='store_true', help='print character only')
    parser.add_argument('-I', '--info', nargs=1, default=[None], help='print character information')

    args = parser.parse_args()

    if args.by:
        by = args.by
    else:
        by = None

    for expr in args.expression:
        search(expr, by, short=args.short)

    return 0