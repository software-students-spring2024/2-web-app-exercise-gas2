from flask import Flask, render_template, request, redirect, abort, url_for, make_response
from authentication import *
from db import * 

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == 'POST':
        if 'login' in request.form:
            return redirect('/login') 
        elif 'sign-up' in request.form:
            return redirect('/signup')
        elif 'play-as-guest' in request.form:
            return redirect('/guest/decks')
    return render_template('start.html')

# Handle authentication related stuff in authentication.py file
@app.route('/login', methods=["GET", "POST"])
def login():
    return authLogin()

@app.route('/signup', methods=["GET", "POST"])
def signup():
    return authSignup()

@app.route("/<username>/decks")
def allDecks(username):
    # would need to first find user in db, but not set up yet
    mainDecks = db.decks.find({})
    return render_template('decks.html', mainDecks=mainDecks)

@app.route("/<username>/create", methods=["POST"])
def createDeck(username):
    # would need to first find user in db, but not set up yet
    title = request.form["title"]
    newDeck = {"title": title, "cards": []}
    db.decks.insert_one(newDeck)
    # would rendirect to template for Cards
    return "created deck"

@app.route("/<username>/<deckTitle>/add", methods=["POST"])
def addCard(username, deckTitle):
    # would need to first find user in db, but not set up yet
    deck = db.decks.find_one({"title": deckTitle})
    newCard = request.form["question"]
    deck["cards"].append(newCard)
    db.decks.update_one({"title": deckTitle}, {"$set": deck})
    # would redirect to template for Cards
    return "added card"

@app.route("/<username>/<deckTitle>/<cardIndex>/edit", methods=["POST"])
def editCard(username, deckTitle, cardIndex):
    # would need to first find user in db, but not set up yet
    deck = db.decks.find_one({"title": deckTitle})
    newCard = request.form["question"]
    deck["cards"][int(cardIndex)] = newCard
    db.decks.update_one({"title": deckTitle}, {"$set": deck})
    # would redirect to template for Cards
    return "edited card"

@app.route("/<username>/<deckTitle>/<cardIndex>/delete")
def deleteCard(username, deckTitle, cardIndex):
    # would need to first find user in db, but not set up yet
    deck = db.decks.find_one({"title": deckTitle})
    deck["cards"].pop(int(cardIndex))
    db.decks.update_one({"title": deckTitle}, {"$set": deck})
    # would redirect to template for Cards
    return "deleted card"

@app.route("/<username>/<deckTitle>/delete")
def deleteDeck(username, deckTitle):
    # would need to first find user in db, but not set up yet
    db.decks.delete_one({"title": deckTitle})
    # would redirect to template for Cards
    return "deleted deck"

# run the app
if __name__ == "__main__":
    FLASK_PORT = os.getenv("FLASK_PORT", "5000")
    app.run(port=FLASK_PORT)
