import os
from flask_restx import Resource,fields
from flask import Flask, request
from pymongo import MongoClient

from decouple import config
from flask_bcrypt import Bcrypt

from dotenv import load_dotenv


# Load environment variables from .env file

# connect with MongoDB
def get_database():
    # Load environment variables from .env file
    
    load_dotenv()

    # connect with MongoDB
    CONNECTION_STRING = os.environ.get("CONNECTION_STRING")
    client = MongoClient(CONNECTION_STRING)
    
    #create the database
    dbname = client['user_list']
    #create collections for user
    collection_name = dbname['users']
    return collection_name


