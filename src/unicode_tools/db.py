import os
import sqlite3
import sys
from pathlib import Path

unicode_sqlite3_database_path = os.path.abspath(os.path.join(os.path.dirname(__file__), f'../../../../share/applications/unicode.db'))
unicode_sqlite3_database_dir = os.path.dirname(unicode_sqlite3_database_path)
if not os.path.exists(unicode_sqlite3_database_dir):
    os.makedirs(unicode_sqlite3_database_dir)
    print(f'Created directory: {unicode_sqlite3_database_dir}', file=sys.stderr)

class Database:

    def create(self):

        def execute(conn, name, dml):
            with Cursor(conn) as cur:
                try:
                    cur.execute(dml)
                    conn.commit()
                    print(f'Created table: {name}')
                except Exception as e:
                    t = type(e)
                    s = str(e)
                    if t == sqlite3.OperationalError and s.endswith(' already exists'):
                        print(f'Table already exists: {name}', file=sys.stderr)
                    else:
                        print(f'Failed to create table: {name}', file=sys.stderr)
                        print(f'{type(e).__name__}: {str(e)}', file=sys.stderr)

        with Connection() as conn:
            execute(conn, 'char', 'create table char(id integer primary key, name text, detail text, codetext text, char text, block text)')
            execute(conn, 'codepoint', 'create table codepoint(char integer, seq integer, code integer, primary key(char, seq))')
            execute(conn, 'char_index', 'create unique index char_index on char(codetext)')

    def delete(self):
        if not os.path.exists(unicode_sqlite3_database_path):
            print(f'No database file: {unicode_sqlite3_database_path}', file=sys.stderr)
        else:
            os.remove(unicode_sqlite3_database_path)
            print(f'Deleted database file: {unicode_sqlite3_database_path}', file=sys.stderr)

    def get_path(self):
        return unicode_sqlite3_database_path

class Connection:

    def __init__(self):
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(unicode_sqlite3_database_path)
        return self.conn

    def __exit__(self, *args):
        if self.conn:
            self.conn.close()

class Cursor:

    def __init__(self, conn):
        self.conn = conn
        self.cur = None

    def __enter__(self):
        self.cur = self.conn.cursor()
        return self.cur

    def __exit__(self, *args):
        if self.cur:
            self.cur.close()
            self.cur = None

class AutoID:

    def init(self):
        self.value = 1
        return self

    def next(self):
        value = self.value
        self.value = self.value + 1
        return value