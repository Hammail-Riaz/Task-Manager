from flask import Blueprint, render_template, redirect
from flask_login import current_user

main = Blueprint("main", __name__, template_folder="templates")

@main.route("/")
def home():
    return render_template("home.html", user=current_user)


