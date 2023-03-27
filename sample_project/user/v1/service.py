import os
from flask_restx import Resource,fields
from flask import Flask, request
from pymongo import MongoClient
from dotenv import load_dotenv
from decouple import config


# Load environment variables from .env file
load_dotenv()
# connect with MongoDB
def get_database():
    #provide mongodb atlas url
    CONNECTION_STRING = config("CONNECTION_STRING")
    #create a connection using MongoClient
    client = MongoClient(CONNECTION_STRING)
    
    #create the database
    dbname = client['user_list']
    #create collections for user
    collection_name = dbname['users']
    return collection_name

