# routes/auth.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash,check_password_hash




auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    from .. import db
    from ..models.user import User 
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

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    from .. import db
    from ..models.user import User 
    if request.method == 'POST':
        email_or_username = request.form['email_or_username'].strip().lower()
        password = request.form['password']

        # Look for user by username or email
        user = User.query.filter(
            (User.email == email_or_username) | (User.username == email_or_username)
        ).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect("/")  
        else:
            return render_template("login.html", error="Invalid credentials.")

    return render_template("login.html")