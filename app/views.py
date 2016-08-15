@App.route('/login', methods=['GET', 'POST'])
def login():
    erorr = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            erorr = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            erorr = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('Yo were logged in')
            return redirect(url_for('public_timeline'))
    return render_template('login.html', error=error)

@App.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('public_timeline'))
