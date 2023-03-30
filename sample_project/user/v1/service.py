from flask_restx import Resource,fields
from flask import Flask, request
from pymongo import MongoClient

from decouple import config



# Load environment variables from .env file

# connect with MongoDB
def get_database():
    # Load environment variables from .env file

    # connect with MongoDB
    CONNECTION_STRING = config("CONNECTION_STRING")
    client = MongoClient(CONNECTION_STRING)
    
    #create the database
    dbname = client['bookstore']
    #create collections for user
    users_collection = dbname['users']
    books_collection = dbname['books']
    return users_collection, books_collection


#create collections for books