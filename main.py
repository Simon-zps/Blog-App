from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.sqlite3'
app.secret_key = '1safdaer34'

app.permanent_session_lifetime = timedelta(seconds=30)

db = SQLAlchemy(app)


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    subtitle = db.Column(db.String(50))
    author = db.Column(db.String(20))
    date = db.Column(db.String(25))
    content = db.Column(db.Text)

    def __init__(self, title, subtitle, author, date, content):
        self.title = title
        self.subtitle = subtitle
        self.author = author
        self.date = date
        self.content = content


@app.route('/base')
def base():
    return render_template('base.html')


@app.route('/')
def index():
    return render_template('index.html', posts=Posts.query.all())


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/post/<int:post_id>')
def post(post_id):
    post = Posts.query.filter_by(id=post_id).first()
    return render_template('post.html', post=post)


@app.route('/viewsql')
def viewsql():
    return render_template('view.html', posts=Posts.query.all())


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'admin' in session:
        flash('Admin already logged in')
        return redirect(url_for('index'))

    if request.method == 'POST':
        if request.form['login'] == 'admin' and request.form['password'] == '1234':
            session['admin'] = 'admin'
            flash('Success, logged in')
        else:
            flash('Login or password is wrong, try again')
        return redirect(url_for('index'))

    return render_template('admin.html')


@app.route('/admin/deletepost/<int:post_id>')
def delete_post(post_id):
    if 'admin' in session:
        post = Posts.query.filter_by(id=post_id).first()
        db.session.delete(post)
        db.session.commit()
        flash('Successfully deleted!')
    else:
        flash('Sign in as an admin first')
    return redirect(url_for('index'))


@app.route('/admin/addpost', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST' and 'admin' in session:
        title = request.form['title']
        subtitle = request.form['subtitle']
        author = request.form['author']
        content = request.form['content']
        str_date = datetime.now().strftime('%d of %B, %Y')

        new_post = Posts(title=title, subtitle=subtitle, author=author, date=str_date, content=content)
        db.session.add(new_post)
        db.session.commit()

        flash('Post successfully added')
        return redirect(url_for('index'))

    elif 'admin' in session:
        return render_template('addpost.html')

    flash('Sign in as an admin first')
    return redirect(url_for('index'))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

