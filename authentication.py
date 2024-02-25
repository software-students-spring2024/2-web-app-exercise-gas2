from flask import render_template

def login():
    return render_template('login.html')

def signup():
    return render_template('signup.html')


