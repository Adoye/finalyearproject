from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create a Flask instance
app = Flask(__name__)
# app.config['TESTING'] = True
# add db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# initialize the db
db = SQLAlchemy(app)

# create model
class Users(db.Model):
      id = db.Column()
      name = db.Column()
      email = db.Column()
      date_added = db.Column()
      
      
# Create a route decorator
@app.route("/")

def index():
    return render_template("index.html")   