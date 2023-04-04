from flask_restx import Resource,fields
from flask import Flask, request
from pymongo import MongoClient

from decouple import config



# Load environment variables from .env file

# connect with MongoDB
def get_database(collection_name):
    # Load environment variables from .env file

    # connect with MongoDB
    CONNECTION_STRING = config("CONNECTION_STRING")
    client = MongoClient(CONNECTION_STRING)
    
    #create the database
    dbname = client['bookstore']
    #create collections for user
    collection = dbname[collection_name]
    return collection


#create collections for books