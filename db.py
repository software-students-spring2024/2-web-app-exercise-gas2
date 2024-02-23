from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

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