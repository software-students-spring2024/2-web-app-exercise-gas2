from flask import render_template, request, redirect, url_for
# from flask_login import LoginManager

# login_manager = LoginManager()

def login():
    if request.method == 'POST':
        ## TODO: Login
        return "Someone pressed the login button huh, I better log you in."
    else:
        return render_template('login.html')

def signup():
    return render_template('signup.html')

