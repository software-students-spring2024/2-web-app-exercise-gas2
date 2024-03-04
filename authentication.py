from flask import render_template, request, redirect, url_for, session, flash
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user
from db import *
from pymongo import *
from werkzeug.security import generate_password_hash, check_password_hash

login_manager = LoginManager()

'''
NOTE: 
To get the active user from a different file or somewhere else 
you need to import flask_login first then you can retrieve the active user with current_user
Example:
    from flask_login import current_user
    if current_user.is_authenticated:
        # Do something with current_user
Also check allDecks function in app.py for example usage
'''
# Automatically implements is_authenticated, is_anonymous, is_active and get_id()
# through UserMixin 
class User(UserMixin):
    def __init__(self, user_id, password):
        self.id = user_id 
        self.password = password 

    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)


@login_manager.user_loader
def load_user(user_id):
    # Find user data in the database
    data = db['users'].find_one({"user_id": user_id})
    if (data):
        return User(data['user_id'], data['password']) # Return user object if found
    else:
        return None


def auth_login():
    collections = db.list_collection_names()
    if request.method == 'POST':
        user_id = request.form["username"]
        password = request.form["password"]
        user = load_user(user_id)
        if user and user.verify_password(password):
            # Redirecting to the appropriate page for the logged in user
            login_user(user)
            return redirect('/' + user_id + '/decks')
        else:
            return render_template('login.html', invalid_login=True) # Login failed - render invalid login message
    else:
        return render_template('login.html', invalid_login=False)


def auth_signup():
    if request.method == 'POST':
        user_id = request.form["username"]
        password = request.form["password"]
        confirm_password =  request.form["confirm-password"]
        if load_user(user_id):
            return render_template('signup.html', username_taken=True, passwords_dont_match=False) # Render username taken message
        elif password != confirm_password:
            return render_template('signup.html', username_taken=False, passwords_dont_match=True) # Render password mismatch message
        else:
            # Generating hashed password for user
            user = User(user_id, generate_password_hash(password))
            # Adding new user to the database
            db['users'].insert_one({"user_id": user.id, "password": user.password, "personalDecks": []})
            login_user(user)
            # Redirect to the appropriate page for the logged in user
            return redirect('/' + user_id + '/decks')

    else:
        return render_template('signup.html', username_taken=False, passwords_dont_match=False)

def auth_logout():
    logout_user()
    return redirect('/') # Redirecting to home page upon logout

