from ast import Sub
from email.policy import default
from enum import unique
import string
from venv import create
from wsgiref.validate import validator
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create a Flask instance
app = Flask(__name__)
# app.config['TESTING'] = True
# add db
app.config['SECRET_KEY'] = "mykey"

class UserForm(FlaskForm):
      name = StringField("Your Name", validator=[DataRequired])
      email = StringField("Your Email", validator=[DataRequired])
      subject = StringField("Your Subject", validator=[DataRequired])
      message = StringField("Message", validator=[DataRequired])
      submit = SubmitField("Submit")

# Creaate a form class
class NamerForm(FlaskForm):
      name = StringField("What is your name", validators=[DataRequired()])
      submit =SubmitField("Submit")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# initialize the db
db = SQLAlchemy(app)

# create model
class Users(db.Model):
      id = db.Column(db.Integer, primary_key=True)
      name = db.Column(db.String(200), nullable=False)
      email = db.Column(db.String(120), nullable=False, unique=True)
      subject = db.Column(db.String(4820), nullable=False, unique=True)
      message = db.Column(db.String(4820), nullable=False, unique=True)
      date_added = db.Column(db.DateTime, default=datetime.utcnow)
      
      # create a string
      def __repr__(self):
           return '<Name %r>' % self.name
      
# Create a route decorator
@app.route('/')

def index():
    return render_template("index.html")   

@app.route('/shop')

def shop():
     return render_template("shop.html")

@app.route('/contact', methods=['GET', 'POST'])

def contact():
      form = UserForm()
      return render_template("contact.html")
