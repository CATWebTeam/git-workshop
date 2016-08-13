import time
import sqlite3

from werkzeug import generate_password_hash

from app import App


# database helper functions
def get_db():
    '''
        connects to the database and returns a sqlite db instance
    '''
    sqlite_db = sqlite3.connect('../twitter.db')
    sqlite_db.row_factory = sqlite3.Row

    return sqlite_db

def init_db(schema):
    '''
        setting up the database with givin schema
    '''
    db = get_db()
    with App.open_resource(schema, mode='r') as f:
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

def db_execute(sql, args=()):
    '''
        execute a sql command with givin args
    '''
    db = get_db()
    db.execute(sql, args)
    db.commit()

# we can consider this as our models replacement
def get_all_twittes():
    '''
        return all twittes with users data for the public timeline
    '''
    twittes = query_db('''
        select twitte.*, user.username from twitte, user
        where twitte.user_id = user.user_id order by twitte.pub_date desc limit ?''',
        [App.config['PER_PAGE']]
    )
    return twittes

def get_user_id(username):
    '''
        get user id using his username
    '''
    id = query_db('''select user_id from user where username = ?''', [username], one=True)
    return id[0] if id else None

def get_user_data(id):
    return query_db('''select username, user_id, email from user where user_id = ?''', [id], one=True)

def get_all_users():
    return query_db('''select * from user''')

def get_user_timeline_twittes(id):
    '''
        get twittes for user's timeline
        his own twittes and twittes from the users he follows
    '''
    return query_db('''
        select twitte.*, user.username from twitte, user
        where twitte.user_id = user.user_id and (
            user.user_id = ? or user.user_id in (select whom_id from follower where who_id = ?)
        )
        order by twitte.pub_date desc limit ?''', [id, id, App.config['PER_PAGE']])

def get_user_profile_data(id):
    '''
        get user's data and twittes for his profile page
    '''
    profile = get_user_data(id)
    twittes = query_db('''select * from twitte where user_id = ?''', [id])
    return {'profile': profile, 'twittes': twittes}

def add_twitte(user_id, text):
    '''
        add a twitte to the database
    '''
    db_execute('''insert into twitte (user_id, twitte_text, pub_date)
    values (?, ?, ?)''', [user_id, text, int(time.time())])

def follow(who_id, whom_id):
    '''
        create a follow entry
    '''
    db_execute('''insert into follower (who_id, whom_id) values (?, ?)''', [who_id, whom_id])

def unfollow(who_id, whom_id):
    '''
        delete a follow entry
    '''
    db_execute('''delete from follower where who_id = ? and whom_id = ?''', [who_id, whom_id])

def check_follow(who_id, whom_id):
    '''
        check follow relation between two users
        returns True or Flase
    '''
    return query_db('''select 1 from follower where follower.who_id = ?
                        and follower.whom_id = ?''',
                        [who_id, whom_id], one=True) is not None

def register_user(username, email, password):
    '''
        register a user in the database
    '''
    db_execute(
        '''insert into user (username, email, pw_hash) values (?, ?, ?)''',
        [username, email, generate_password_hash(password)],
    )
