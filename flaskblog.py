from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm


app = Flask(__name__)

app.config['SECRET_KEY'] = 'eb36e878d9188f88d2e3684bf8317d3d'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

updates = [
	{
		'Author': 'Oluwatobi',
		'Title': 'Engineering Guide',
		'Content': 'Guides to Engineering Success.',
		'Date_Posted': 'April 19, 2021'
	},
	{
		'Author': 'Johnson',
		'Title': 'Website Development',
		'Content': 'Guides to website Development.',
		'Date_Posted': 'April 19, 2021'
	}
]
@app.route("/")
def hello_world():
    return "<b>Login Successful!<br>You are now elligible for the application.</b>"

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)

@app.route("/about")
def about():
    return '''<!DOCTYPE html>
    <html>
    	<head>
    		<style>
    			a input {background-color: red;}
    		</style>
    	</head>
    	<body>
    		<h1>About us</h1>
    		<p>We implore every registered candidate to our website training.
    	In this training a lot of opportunities and advantages will be made available for you.
    		</p>
    		<h3 style='color: blue;'>This training was organised by <b>GTECH</b> web developer.
    		We are admonishing you today not be the only one to register for this program but invite as many as possible people 
    		to register for this program, so that you we be eligible to get many opportunities like discount sales and promo from us.
    		<h4>To proceed click the button below.<br><a href='http://127.0.0.1:5000/'><input type='button' value='continue'></a>
    		</h3>
    	</body>
    </html>
    '''
@app.route("/home")
def home():
    return render_template('home.html', posts=updates)
@app.route("/about_us")
def about_us():
    return render_template('about.html', title='Website', posts=updates)

if __name__ == '__main__':
    app.run(debug=True)

