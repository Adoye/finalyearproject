from flask import Flask, render_template


# Create a Flask instance
app = Flask(__name__)
# app.config['TESTING'] = True

# Create a route decorator
@app.route("/")

def index():
    return render_template("index.html")