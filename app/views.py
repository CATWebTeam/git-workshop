from flask import Flask, request, session, url_for, redirect, \
render_template, abort, g, flash, _app_ctx_stack

from app import App
from app import db_utils
from app import config

@App.route('/')
def public_timeline():
    return render_template('public_timeline.html', flashes=db_utils.get_all_twittes())

@App.route('/register', methods=['GET', 'POST']) # akef
def register():
    """Registers the user."""
    #if g.user: not now
    #    return redirect(url_for('timeline'))
    error = None
    if request.method == 'POST':
        if not request.form['username']:
            error = 'You have to enter a username'
        elif not request.form['email'] or \
                '@' not in request.form['email']:
            error = 'You have to enter a valid email address'
        elif not request.form['password']:
            error = 'You have to enter a password'
        elif request.form['password'] != request.form['password2']:
            error = 'The two passwords do not match'
        elif db_utils.get_user_id(request.form['username']) is not None:
            error = 'The username is already taken'
        else:
            db_utils.register_user(request.form['username'],request.form['email'],request.form['password'])
            flash('You were successfully registered and can login now')
            return redirect(url_for('public_timeline'))
    return render_template('signup.html', error=error)
