from ast import Sub
from email.policy import default
from enum import unique
import string
from venv import create
from wsgiref.validate import validator
from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, email_validator, Length
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_admin import Admin

# Create a Flask instance
app = Flask(__name__)
# app.config['TESTING'] = True
# add db

admin = Admin(app)
app.config['SECRET_KEY'] = "mykey"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/c/Users/antho/Documents/login-example/database.db'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
# class UserForm(FlaskForm):
#       name = StringField("Your Name", validator=[DataRequired])
#       email = StringField("Your Email", validator=[DataRequired])
#       subject = StringField("Your Subject", validator=[DataRequired])
#       message = StringField("Message", validator=[DataRequired])
#       submit = SubmitField("Submit")

# Creaate a form class
# class NamerForm(FlaskForm):
#       name = StringField("What is your name", validators=[DataRequired()])
#       submit =SubmitField("Submit")

# old sql
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# new sql
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Qwerty@123@localhost/our_users'
# initialize the db
# db = SQLAlchemy(app)

# create model
# class Users(db.Model):
#       id = db.Column(db.Integer, primary_key=True)
#       name = db.Column(db.String(200), nullable=False)
#       email = db.Column(db.String(120), nullable=False, unique=True)
#       subject = db.Column(db.String(4820), nullable=False, unique=True)
#       message = db.Column(db.String(4820), nullable=False, unique=True)
#       date_added = db.Column(db.DateTime, default=datetime.utcnow)
#       password_hash = db.Column(db.String(128))
      
#       @property
#       def password(self):
#             raise AttributeError('password is not a readable attribute!')
      
#       @password.setter
#       def password(self, password):
#             self.password_hash = generate_password_hash(password)
            
#       def verify_password(self, password):
#             return check_password_hash(self.password_hash, password)
      
      
      
      # create a string
      # def __repr__(self):
      #      return '<Name %r>' % self.name
      
# Create a route decorator
@app.route('/')

def index():
    return render_template("index.html")   

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))

        return '<h1>Invalid username or password</h1>'
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return '<h1>New user has been created!</h1>'
        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('signup.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.username)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/shop')

def shop():
     return render_template("shop.html")

@app.route('/contact', methods=['GET', 'POST'])

def contact():
     return render_template("contact.html")

if __name__ == '__main__':
    app.run(debug=True)