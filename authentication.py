from flask import render_template, request, redirect, url_for, session
from flask_login import LoginManager
from db import *


login_manager = LoginManager()

class User():
    def __init__(self, username, password, is_authenticated, is_active, is_anonymous):
        self.is_authenticated = is_authenticated
        self.is_active = is_active
        self.is_anonymous = is_anonymous

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

def authLogin():
    if request.method == 'POST':
        ## TODO: Login
        return "Someone pressed the login button huh, I better log you in."
    else:
        return render_template('login.html')

def authSignup():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
    else:
        return render_template('signup.html')

