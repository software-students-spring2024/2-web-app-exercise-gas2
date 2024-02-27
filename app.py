from flask import Flask, render_template, request, redirect, abort, url_for, make_response
from authentication import *
from db import * 
import random

app = Flask(__name__)
login_manager.init_app(app)

# Secret key for login session management, set this up in your .env file 
load_dotenv()
app.secret_key = os.getenv("SECRET_KEY")


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
    return auth_login()

@app.route('/signup', methods=["GET", "POST"])
def signup():
    return auth_signup()

@app.route("/<username>/decks")
def allDecks(username):
    # would need to first find user in db, but not set up yet
    if username == "guest":
        mainDecks = db.decks.find({})
        return render_template('decks.html', mainDecks=mainDecks)
    else:
        return "to do: for users"

@app.route("/<username>/<deckTitle>")
def displayDeck(username, deckTitle):
    if username == "guest":
        # get the list of cards for the deck
        currentDeck = db.decks.find_one({"title": deckTitle})
        cardList = currentDeck['cards']
        # generate a random index to generate a random card
        index = random.randint(0, len(cardList)-1)
        question = cardList[index]
        # remove card to avoid repetition
        cardList.pop(index) 

        return render_template('card.html', deckTitle=deckTitle, question=question, username=username)

        if 'add-card' in request.form:
            return redirect('/username/deckTitle/add')
        elif 'edit' in request.form:
            return redirect('/username/deckTitle/index/add')
    return "temp"

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

