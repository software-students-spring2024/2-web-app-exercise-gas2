from flask import render_template, request, redirect, url_for, session
from flask_login import LoginManager, UserMixin
from db import *
from pymongo import *
from werkzeug.security import generate_password_hash, check_password_hash

login_manager = LoginManager()

@login_manager.user_loader
def load_user(username):
    return db['users'].find_one({"username": username})

class User(UserMixin):
    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password) 

    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)

def auth_login():
    collections = db.list_collection_names()
    if request.method == 'POST':
        for collection in collections:
            print("Collection name: " + collection)

        ## TODO: Login
        return "Someone pressed the login button huh, I better log you in."
    else:
        return render_template('login.html')

def auth_signup():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        confirm_password =  request.form["confirm-password"]
        if (load_user(username)):
            return render_template('signup.html', username_taken=True, passwords_dont_match=False)
        elif(password != confirm_password):
            return render_template('signup.html', username_taken=False, passwords_dont_match=True)
        else:
            return "Username doesn't exist, we should probably sign you up."
    else:
        return render_template('signup.html', username_taken=False, passwords_dont_match=False)

