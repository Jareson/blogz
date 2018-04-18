from flask import Flask, request, redirect, render_template, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:Blogz!@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = "sUtIm6jEdz"

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(255))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, email, password):
        self.email = email
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup']
    if request.endpoint not in allowed_routes and "email" not in session:
        return redirect('/login')


@app.route('/blog', methods=['POST', 'GET'])
def blog():
    owner = User.query.filter_by(email=session['email']).first()
    blog_entries = Blog.query.filter_by(owner=owner).all()
    # blog_id = request.args.get('id')
    # blog_query = Blog.query.filter_by(id=blog_id).first()
    return render_template("blog.html", blog_entries=blog_entries)

@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    title = ""
    body = ""
    owner = User.query.filter_by(email=session['email']).first()
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        if not title and not body:
            flash("Blog must contain a title and body", "error")
        elif not title:
            flash("Blog must contain a title", "error")
        elif not body:
            flash("Blog must contain a body", "error")
        else:
            new_entry= Blog(title, body, owner)
            db.session.add(new_entry)
            db.session.commit()
            # new_entry = Blog.query.filter_by(title=new_entry.title, body=new_entry.body).first()
            # print(new_entry)
            # new_id = str(new_entry.id)
            # print(new_id)
            return redirect('/blog')
    return render_template('newpost.html', title=title, body=body)

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']
        existing_user = User.query.filter_by(email=email).first()
        if not email or not password:
            flash('Must enter an email and a password', 'error')
        elif password != verify:
            flash('Passwords do not match', 'error')
        elif not existing_user:
            new_user = User(email, password)
            db.session.add(new_user)
            db.session.commit()
            session['email'] = email
            return redirect('/newpost')
        else:
            flash('Duplicate User', 'error')

    return render_template('signup.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['email'] = email
            flash("Logged in")
            return redirect('/newpost')
        elif not user:
            flash('User does not exist', 'error')
        elif user.password != password:
            flash('Incorrect password', 'error')
            
    return render_template('login.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/logout')
def logout():
    del session['email']
    return redirect('/blog')

@app.route('/', methods=['POST', 'GET'])
def home():
    return redirect('/blog')

if __name__ == '__main__':
    app.run()