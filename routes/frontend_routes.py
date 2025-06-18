from flask import Blueprint, render_template
from datetime import datetime

frontend = Blueprint("frontend", __name__)

@frontend.route("/")
def home():
    return render_template("index.html" , now=datetime.now() )

@frontend.route("/about")
def about():
    return render_template("about.html")

@frontend.route("/projects")
def projects():
    return render_template("portfolio.html")

@frontend.route("/contact")
def contact():
    return render_template("contact.html")
