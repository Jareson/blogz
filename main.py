from flask import Flask, request, redirect, render_template, flash
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

    def __init__(self, title, body):
        self.title = title
        self.body = body

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120))
    password = db.Column(db.String(120))

    def __init__(self, email, password)
        self.email = email
        self.password = password




@app.route('/blog', methods=['POST', 'GET'])
def blog():
    blog_entries = Blog.query.all()
    blog_id = request.args.get('id')
    blog_query = Blog.query.filter_by(id=blog_id).first()
    return render_template("blog.html", blog_entries=blog_entries, blog_query=blog_query)

@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    title = ""
    body = ""
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
            new_entry= Blog(title, body)
            db.session.add(new_entry)
            db.session.commit()
            new_entry = Blog.query.filter_by(title=new_entry.title, body=new_entry.body).first()
            print(new_entry)
            new_id = str(new_entry.id)
            print(new_id)
            return redirect('/blog?id=' + new_id)
    return render_template('newpost.html', title=title, body=body)

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/logout' methods=['POST'])
def logout():
    return redirect('/blog')

@app.route('/', methods=['POST', 'GET'])
def home():
    return redirect('/blog')

if __name__ == '__main__':
    app.run()