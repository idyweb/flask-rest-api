#import libraries
import bcrypt
from flask import Flask, jsonify, request
from flask_jwt_extended import (JWTManager, create_access_token, get_jwt_identity, jwt_required)
from flask_restx import Api, Namespace, Resource, fields
from pymongo import MongoClient

from sample_project.user import auth_namespace, ns
from sample_project.user.v1.service import get_database

# create signup model
signup_model = auth_namespace.model(
    "SignUp", {
        "id": fields.Integer(),
        "username": fields.String(required=True),
        "email": fields.String(required=True),
        "password": fields.String(required=True),
    }
)

# create login model
login_model = auth_namespace.model(
    "Login", {
        "username": fields.String(required=True),
        "email": fields.String(required=True),
        "password": fields.String(required=True),
    }
)

@auth_namespace.route("/signup")
class Signup(Resource):
    @auth_namespace.expect(signup_model)
    def post(self):
        """
        create a new user account
        """
        data = request.get_json()

        # create a new user object
        new_user = {
            "username": data['username'],
            "email": data['email'],
            "password": bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
        }
        email = data['email']
        username = data['username']

        # insert the user data into the MongoDB database
        try:
            users_collection, books_collection = get_database()
            user = users_collection.find_one(
                {
                    "$or": [{"username": username}, {"email": email}]
                }
            )
            if not user:
                users_collection.insert_one(new_user)
                return {"message": "User created successfully"}, 201
            else:
                return {"message": "User already exists"}, 403
        except Exception as e:
            return {"message": f"Error creating user: {str(e)}"}, 500


    
@auth_namespace.route("/login")
class Login(Resource):
    @auth_namespace.expect(login_model)
    def post(self):
        """
        Log in an existing user
        """
        data = request.get_json()
        
        username = data['username']
        email = data['email']
    

        # check if user exists in database
        users_collection, books_collection = get_database()
        user = users_collection.find_one(
                {
                    "$or": [{"email":email},{"username":username}]
                }
            )
        if not user:
            return {"message": "Invalid email or password"}, 401
        
        try:
        # check if password matches
            if not bcrypt.checkpw(data["password"].encode('utf-8'), user["password"].encode('utf-8')):
                return {"message": "Invalid email or password"}, 401
        except Exception as e:
            return {"message": f"Error checking password: {str(e)}"}, 500

        # create an access token for the user
        access_token = create_access_token(identity=str(user["_id"]))

        # return the access token
        return {"access_token": access_token}, 200
