from flask import Flask, render_template, request, url_for, flash, redirect
import sqlite3
from werkzeug.exceptions import abort
import json



app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'




def check():
    with open('users.json') as f:
        users = json.load(f)

    for index in users:
        if (index['name']== username) and (index['password'] == password):
            print(index['name'],username,index['password'],password)
            return True

    print(index['name'],username,index['password'],password)
    return False


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

@app.route('/')
def index():
    try:
        username
    except:
        username = 'andrej'
    print(username)
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    posts.reverse()
    return render_template('index.html',posts=posts,username = username)

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)

@app.route('/create', methods=('GET', 'POST'))
def create():
    test_user = check()
    if test_user == False:
            flash('No user')
            return redirect(url_for('index'))

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')

        else:

            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',(title, content))
            conn.commit()
            conn.close()
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    test_user = check()
    if test_user == False:
            flash('No user')
            return redirect(url_for('index'))

    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))

@app.route('/login', methods=('GET', 'POST'))
def login():

    if request.method == 'POST':
         global username
         global password
         username = request.form['uname']
         password = request.form['psw']



         if (not username) or (not password):
             flash('fild is required!')
         else:
             test = check()
             print(test)
             if test == True:
                 return redirect(url_for('index'))
             if test == False:
                 return render_template('login.html')
    return render_template('login.html')


@app.route('/logout')
def logout():
    global username
    global password
    username = ''
    password = ''
    print(username,password)
    return redirect(url_for('index'))
