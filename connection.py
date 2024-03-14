from pymongo import MongoClient

# Establish connection to MongoDB
client = MongoClient("mongodb://localhost:27017/")

# Access the database
db = client.mydb
