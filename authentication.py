from flask import render_template, request, redirect, url_for, session
from flask_login import LoginManager
import app


login_manager = LoginManager()

class User():
    def __init__(self, is_authenticated, is_active, is_anonymous):
        self.is_authenticated = is_authenticated
        self.is_active = is_active
        self.is_anonymous = is_anonymous


def login(db):
    print(db)
    if request.method == 'POST':
        ## TODO: Login
        return "Someone pressed the login button huh, I better log you in."
    else:
        return render_template('login.html')

def signup(db):
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
    else:
        return render_template('signup.html')

