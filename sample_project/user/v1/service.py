from flask_restx import Resource,fields
from flask import Flask, request
from pymongo import MongoClient
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()
# connect with MongoDB
def get_database():
    #provide mongodb atlas url
    CONNECTION_STRING = "mongodb+srv://idyvalour:123coragem@books.s1ptkl1.mongodb.net/?retryWrites=true&w=majority" 
    #create a connection using MongoClient
    client = MongoClient(CONNECTION_STRING)
    
    #create the database
    dbname = client['user_list']
    #create collections for user
    collection_name = dbname['users']
    return collection_name
