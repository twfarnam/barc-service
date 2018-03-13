import flask
import os
import sqlite3


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def connect_db():
    path = os.path.join(os.path.dirname(__file__), '../../barc.db')
    print path
    rv = sqlite3.connect(path)
    rv.row_factory = dict_factory
    return rv

db = None
def get_db():
    global db
    if db == None:
        db = connect_db()
    return db

