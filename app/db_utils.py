import sqlite3
from datetime import datetime

from app import App

# database helper functions
def get_db():
    '''
        connects to the database and returns a sqlite db instance
    '''
    sqlite_db = sqlite3.connect(App.config['DATABASE'])
    sqlite_db.row_factory = sqlite3.Row

    return sqlite_db

def init_db(schema):
    '''
        setting up the database with givin schema
    '''
    db = get_db()
    with App.open_resource(schema, mode=r) as f:
        db.cursor().executescript(f.read())
    db.commit()

def query_db(query, args=(), one=False):
    '''
        Execute a sql query with givin args,
        args:
            - query: sql query to be executed
            - args: argumnets for the sql query
            - one : if True return the first value of the query
                    else return all values
    '''
    cursor = get_db().execute(query, args)
    values = cursor.fetchall()

    return (values[0] if values else None) if one else values

# we can consider this as our models replacement
def get_all_twittes():
    '''
        return all twittes from all users for the public timeline
    '''
    twittes = query_db('''
        select * from twittes order by twittes.pub_date desc limit ?''',
        App.config['PER_PAGE'])
    return twittes
