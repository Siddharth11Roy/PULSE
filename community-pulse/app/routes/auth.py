# routes/auth.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from .. import db
from ..models.user import User 


auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username'].strip()
        email = request.form['email'].strip().lower()
        phone = request.form['phone'].strip()
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Password match check
        if password != confirm_password:
            return render_template("signup.html", error="Passwords do not match.")

        # Duplicate check
        if User.query.filter((User.username == username) | (User.email == email) | (User.phone == phone)).first():
            return render_template("signup.html", error="User with these credentials already exists.")

        # Create new user
        hashed_pw = generate_password_hash(password)
        new_user = User(
            username=username,
            email=email,
            phone=phone,
            password=hashed_pw,
        )

        db.session.add(new_user)
        db.session.commit()

        return render_template("signup.html", success="Signup successful! You can now log in.")

    return render_template("signup.html")

@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')