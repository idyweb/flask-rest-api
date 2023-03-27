#import libraries
import os
import json
from datetime import datetime, timedelta, timezone

from flask import Flask, jsonify, request
from flask_restx import Resource, fields, Namespace, Api
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
    JWTManager
)
from pymongo import MongoClient
import bcrypt

from sample_project.user import ns, auth_namespace
from sample_project.user.v1.service import get_database

app = Flask(__name__)

# define the user model
user = ns.model('User', {
    'id': fields.Integer,
    'name': fields.String(required=True, min_length=1),
    'email': fields.String(required=True, min_length=5),
})

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

        # insert the user data into the MongoDB database
        try:
            collection = get_database()
            users = collection.find_one(
                {
                    "$or": [{"username": data["username"]}, {"email": data["email"]}]
                }
            )
            if not users:
                collection.insert_one(new_user)
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
        
        email = data['email']
        password = data['password']

        # check if user exists in database
        collection = get_database()
        user = collection.find_one(
                {
                    "$or": [{"email":email},{"password":password}]
                }
            )
        if not user:
            return {"message": "Invalid email or password"}, 401

        # check if password matches
        if not bcrypt.checkpw(data["password"].encode('utf-8'), user["password"].encode('utf-8')):
            return {"message": "Invalid email or password"}, 401

        # create an access token for the user
        access_token = create_access_token(identity=str(user["_id"]))

        # return the access token
        return {"access_token": access_token}, 200

    

@ns.route('/users', methods=['POST'])
class User(Resource):

    @ns.expect(user, validate=True)
    @ns.marshal_with(user, envelope='user')
    def post(self):
        data = request.json
        data['id'] = 1
        return data, 201


@ns.route('/users/<string:user_id>', methods=['GET'])
class UserDetail(Resource):
    @ns.marshal_with(user, envelope='user')
    def get(self, user_id):
        if user_id == '1':
            return {
                'id': 1,
                'name': 'John Doe',
                'email': 'john.doe@example.com'
            }
        return {}, 404