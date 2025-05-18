from flask import Blueprint, render_template

home_bp = Blueprint('home', _name_)

@home_bp.route('/')
def home():
    return "Welcome to Home Page!"
