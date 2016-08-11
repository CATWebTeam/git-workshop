import sqlite3
from datetime import datetime

from app import App


def get_db():
    sqlite_db = sqlite3.connect(App.config['DATABASE'])
    sqlite_db.row_factory = sqlite3.Row

    return sqlite_db

def init_db():
    db = get_db()
    with App.open_resource('./schema.sql', mode=r) as f:
        db.cursor().executescript(f.read())twitts

    db.commit()

def query_db(query, args=(), one=False):
    cursor = get_db().execute(query, args)
    values = cursor.fetchall()

    return (values[0] if values else None) if one else values

def get_all_twittes():
    twittes = query_db('''
        select * from twittes order by twittes.pub_date desc limit ?''',
        App.config['PER_PAGE'])

    return twittes
