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
    dbname = client['user_list']
    #create collections for user
    collection_name = dbname['users']
    return collection_name


