from flask import Flask, render_template, request, redirect, abort, url_for, make_response
from dotenv import load_dotenv
import os
import pymongo
from pymongo import MongoClient

load_dotenv()

app = Flask(__name__)

uri = os.getenv("MONGO_URI")
db_name = os.getenv("MONGO_DBNAME")

# Create a new client and connect to the server
client = MongoClient(uri)
db = client[db_name]

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Connected to MongoDB!")
except Exception as e:
    print("MongoDB connection error:", e)

@app.route("/")
def home():
    return render_template('mainScreen.html')

@app.route("/<username>/decks")
def allDecks(username):
    # would need to first find user in db, but not set up yet
    # would redirect to template for Decks
    return f'{username} decks'

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

# run the app
if __name__ == "__main__":
    FLASK_PORT = os.getenv("FLASK_PORT", "5000")
    app.run(port=FLASK_PORT)