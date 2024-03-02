from flask import Flask, render_template, request, redirect, abort, url_for, make_response
from flask_login import current_user
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
    if username == "guest":
        mainDecks = db.decks.find({})
        return render_template('decks.html', mainDecks=mainDecks, isAuth=False)
    else:
        # authenticate user
        if (not current_user.is_authenticated or current_user.id != username):
            return redirect('/login')
        user = db.users.find_one({'user_id': current_user.id})
        mainDecks = db.decks.find({})
        return render_template('decks.html', username=username, isAuth=True, mainDecks=mainDecks, personalDecks=user['personalDecks'])

@app.route("/<username>/<deckTitle>")
def displayDeck(username, deckTitle):
    if username == "guest":
        # get the list of cards for the deck
        currentDeck = db.decks.find_one({"title": deckTitle})
        cardList = currentDeck['cards']
        # shuffle deck
        random.shuffle(cardList)
        return render_template('card.html', deckTitle=deckTitle, username=username, cardList=cardList)
    else:
        # authenticate user
        if (not current_user.is_authenticated or current_user.id != username):
            return redirect('/login')
        # TODO: id is not being generated, some problem
        currentDeck = db.users.find_one({"user_id": username, "personalDecks.title": deckTitle}, {"personalDecks.$": 1}).get("personalDecks")[0]
        # if the deck is not found in the users deck, look for in main
        if not currentDeck:
            currentDeck = db.decks.find_one({"title": deckTitle})
        cardList = currentDeck['cards']
        # shuffle deck
        random.shuffle(cardList)
        return render_template('card.html', deckTitle=deckTitle, username=username, cardList=cardList)

# TODO: change createDeck to addDeck for naming consistency
@app.route("/<username>/create", methods=["POST"])
def createDeck(username):
    # authenticate user
    if (not current_user.is_authenticated or current_user.id != username):
        return redirect('/login')
    title = request.form["title"]
    newDeck = {"title": title, "cards": []}
    db.users.update_one({"user_id": username}, {"$push": {"personalDecks": newDeck}})
    # would rendirect to template for Cards
    return "created deck"

# since shuffled, maybe should be cardQuestion instead of cardIndex?
@app.route("/<username>/<deckTitle>/<cardIndex>/add", methods=["POST"])
def addCard(username, deckTitle, cardIndex):
    # authenticate user
    if (not current_user.is_authenticated or current_user.id != username):
        return redirect('/login')
    # would need to first find user in db, but not set up yet
    deck = db.decks.find_one({"title": deckTitle})
    newCard = request.form["question"]
    deck["cards"].insert(int(cardIndex), newCard)
    db.decks.update_one({"title": deckTitle}, {"$set": deck})
    # would redirect to template for Cards
    return "added card"

@app.route("/<username>/<deckTitle>/<cardIndex>/edit", methods=["POST"])
def editCard(username, deckTitle, cardIndex):
    # authenticate user
    if (not current_user.is_authenticated or current_user.id != username):
        return redirect('/login')
    # would need to first find user in db, but not set up yet
    deck = db.decks.find_one({"title": deckTitle})
    newCard = request.form["question"]
    deck["cards"][int(cardIndex)] = newCard
    db.decks.update_one({"title": deckTitle}, {"$set": deck})
    # would redirect to template for Cards
    return "edited card"

@app.route("/<username>/<deckTitle>/<cardIndex>/delete")
def deleteCard(username, deckTitle, cardIndex):
    # authenticate user
    if (not current_user.is_authenticated or current_user.id != username):
        return redirect('/login')
    # would need to first find user in db, but not set up yet
    deck = db.decks.find_one({"title": deckTitle})
    deck["cards"].pop(int(cardIndex))
    db.decks.update_one({"title": deckTitle}, {"$set": deck})
    # would redirect to template for Cards
    return "deleted card"

@app.route("/<username>/<deckTitle>/delete")
def deleteDeck(username, deckTitle):
    # authenticate user
    if (not current_user.is_authenticated or current_user.id != username):
        return redirect('/login')
    # would need to first find user in db, but not set up yet
    db.decks.delete_one({"title": deckTitle})
    # would redirect to template for Cards
    return "deleted deck"

# run the app
if __name__ == "__main__":
    FLASK_PORT = os.getenv("FLASK_PORT", "5000")
    app.run(port=FLASK_PORT)

