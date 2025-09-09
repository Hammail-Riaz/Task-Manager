from flask import Blueprint, redirect , render_template, url_for, flash
from .forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from ...extensions import db
from .models import User
from flask_login import login_user, logout_user, current_user, login_required

auth = Blueprint("auth", __name__, template_folder="templates")

@auth.route("/register", methods=["POST", "GET"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        hash_password = generate_password_hash(password)
        
        db.session.add(
            User(
                username=username,
                password=hash_password
            )
            )
        db.session.commit()
    
        flash(f"{username} Registered Succcessfully!", "success")

        return redirect(url_for("auth.login"))
    return render_template("register.html", form=form)

@auth.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        user = User.query.filter_by(username=username).first()
        
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash(f"{username} Logged In Successfully!", 'success')
            return redirect(url_for("profile.dashboard"))
        
        else:
            flash(f"Invalid Username or Password", 'danger')
            return redirect(url_for('auth.login'))
        
    return render_template("login.html", form= form)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.home"))
    





        