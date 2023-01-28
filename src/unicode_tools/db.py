import os
import sqlite3
import sys

unicode_sqlite3_database_filename = 'unicode.db'
unicode_sqlite3_database_path = os.path.abspath(os.path.join(os.path.dirname(__file__), f'../../../../share/applications/{unicode_sqlite3_database_filename}'))

class Database:

    def create(self):
        created = False
        with Connection() as conn:
            with Cursor(conn) as cur:
                try:
                    table = 'char'
                    cur.execute('create table char(code integer primary key, name text, char text)')
                    conn.commit()
                    created = True
                except Exception as e:
                    t = type(e)
                    s = str(e)
                    if t == sqlite3.OperationalError and s.endswith(' already exists'):
                        print(f'Tables already exist', file=sys.stderr)
                    else:
                        print(f'Failed to create table {table}', file=sys.stderr)
                        print(f'{type(e).__name__}: {str(e)}', file=sys.stderr)
        if created:
            print(f'Created tables')

    def delete(self):
        if not os.path.exists(unicode_sqlite3_database_path):
            print(f'No database file: {unicode_sqlite3_database_path}', file=sys.stderr)
        else:
            os.remove(unicode_sqlite3_database_path)
            print(f'Deleted database file: {unicode_sqlite3_database_path}', file=sys.stderr)

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