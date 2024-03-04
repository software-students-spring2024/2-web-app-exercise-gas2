from flask import Flask, render_template, request, redirect, abort, url_for, make_response
from flask_login import current_user
from authentication import *
from db import * 
import random
import json

app = Flask(__name__)
login_manager.init_app(app)

# Secret key for login session management, set this up in your .env file 
load_dotenv()
app.secret_key = os.getenv("SECRET_KEY")

@app.route("/", methods=["GET", "POST"])
def home():
    #  Handle requests for the home page
    if request.method == 'POST':
        if 'login' in request.form:
            return redirect(url_for('login')) 
        elif 'sign-up' in request.form:
            return redirect(url_for('signup'))
        elif 'play-as-guest' in request.form:
            return redirect(url_for('allDecks', username='guest', isAuth=False))
    if request.method == 'GET':
        if (current_user.is_authenticated):
            return redirect(url_for('allDecks', username=current_user.id, isAuth=True))
    return render_template('start.html')

# Handle authentication related stuff in authentication.py file
@app.route('/login', methods=["GET", "POST"])
def login():
    return auth_login()

@app.route('/signup', methods=["GET", "POST"])
def signup():
    return auth_signup()

@app.route('/logout', methods=["GET", "POST"])
def logout():
    return auth_logout()

# Page to display all decks
@app.route("/<username>/decks")
def allDecks(username):
    if username == "guest":
        mainDecks = db.decks.find({}) # Get all guest user decks
        return render_template('decks.html', mainDecks=mainDecks, isAuth=False)
    else:
        # Authenticate user
        if (not current_user.is_authenticated or current_user.id != username):
            return redirect(url_for('login'))
        user = db.users.find_one({'user_id': current_user.id})
        # Get all public and personal decks
        mainDecks = db.decks.find({})
        personalDecks = user['personalDecks']
        return render_template('decks.html', username=username, isAuth=True, mainDecks=mainDecks, personalDecks=personalDecks)

@app.route("/<username>/<deckTitle>")
def displayDeck(username, deckTitle):
    if username == "guest":
        # get the list of cards for the deck
        currentDeck = db.decks.find_one({"title": deckTitle})
        cardList = currentDeck['cards']
        # shuffle deck
        random.shuffle(cardList)
        return render_template('card.html', deckTitle=deckTitle, username=username, cardList=json.dumps(cardList), isAuth=False)
    else:
        # authenticate user
        if (not current_user.is_authenticated or current_user.id != username):
            return redirect(url_for('login'))
        # TODO: id is not being generated, some problem
        currentDeck = db.users.find_one(
            {"user_id": username, "personalDecks.title": deckTitle}, 
            {"personalDecks.$": 1}
        ).get("personalDecks")[0] # Get user's personal deck
        # if the deck is not found in the users deck, look for in main
        if not currentDeck:
            currentDeck = db.decks.find_one({"title": deckTitle})
        cardList = currentDeck['cards']
        # shuffle deck
        random.shuffle(cardList)
        return render_template('card.html', deckTitle=deckTitle, username=username, cardList=json.dumps(cardList), isAuth=True)

# TODO: change createDeck to addDeck for naming consistency
# Page for creating a new deck
@app.route("/<username>/create", methods=["POST"])
def createDeck(username):
    # authenticate user
    if (not current_user.is_authenticated or current_user.id != username):
        return redirect(url_for('login'))
    title = request.form["title"]

    # Check if the title already exists in personalDecks
    existingDeck = db.users.find_one({"user_id": username, "personalDecks.title": title})
    # if title already exists, don't create new deck
    if existingDeck:
        return redirect(url_for('allDecks', username=username))
    
    newDeck = {"title": title, "cards": []}
    db.users.update_one({"user_id": username}, {"$push": {"personalDecks": newDeck}})
    # would rendirect to decks
    # TODO: is there a way to not have to refresh the page and add the new deck 
    return redirect(url_for('allDecks', username=username))

# Page to add a card to a deck
@app.route("/<username>/<deckTitle>/<cardIndex>/add", methods=["POST"])
def addCard(username, deckTitle, cardIndex):
    # authenticate user
    if (not current_user.is_authenticated or current_user.id != username):
        return redirect(url_for('login'))
    newCard = request.form["question"]
    # Adding a new card to the deck
    db.users.update_one(
        {"user_id": username, "personalDecks.title": deckTitle},
        {"$push": {"personalDecks.$.cards": newCard}}
    )
    # would redirect to template for Cards
    # TODO: is there a way to not have to refresh the page and show the added card 
    return redirect(url_for('displayDeck', username=username, deckTitle=deckTitle))

# Page to edit a card in the deck
@app.route("/<username>/<deckTitle>/<cardIndex>/edit", methods=["POST"])
def editCard(username, deckTitle, cardIndex):
    # authenticate user
    # if (not current_user.is_authenticated or current_user.id != username):
    #     return redirect(url_for('login'))
    newCard = request.form["question"]
    oldCard = request.form["oldQuestion"]
    # Editing a card in the deck
    db.users.update_one(
        {"user_id": username, "personalDecks.title": deckTitle},
        {"$set": {"personalDecks.$[deck].cards.$[card]": newCard}},
        array_filters=[{"deck.title": deckTitle}, {"card": oldCard}]
    )
    # would redirect to template for Cards
    # TODO: is there a way to not have to refresh the page and show the edited card 
    return redirect(url_for('displayDeck', username=username, deckTitle=deckTitle))

@app.route("/<username>/<deckTitle>/<cardIndex>/delete", methods=["POST"])
def deleteCard(username, deckTitle, cardIndex):
    # authenticate user
    if (not current_user.is_authenticated or current_user.id != username):
        return redirect(url_for('login'))
    cardQuestion = request.form["question"]
    db.users.update_one(
        {"user_id": username, "personalDecks.title": deckTitle},
        {"$pull": {"personalDecks.$.cards": cardQuestion}}
    )
    # TODO: is there a way to not have to refresh the page and show the previous card 
    return redirect(url_for('displayDeck', username=username, deckTitle=deckTitle))

# Page to delete card from a deck
@app.route("/<username>/<deckTitle>/delete", methods=['GET', 'POST'])
def deleteDeck(username, deckTitle):
    # authenticate user
    if (not current_user.is_authenticated or current_user.id != username):
        return redirect(url_for('login'))
    # Deleting a card from the deck
    db.users.update_one({"user_id": username}, {"$pull": {"personalDecks": {"title": deckTitle}}})
    # TODO: is there a way to not have to refresh the page when deleting deck
    return redirect(url_for('allDecks', username=username))

# run the app
if __name__ == "__main__":
    FLASK_PORT = os.getenv("FLASK_PORT", "5000")
    app.run(port=FLASK_PORT)

