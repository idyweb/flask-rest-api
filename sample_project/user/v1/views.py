#import libraries
import os
from flask_restx import Resource, fields,Namespace,Api 
from flask import request

from sample_project.user import ns, auth_namespace
from sample_project.user.v1.service import get_database

import json

from datetime import datetime, timedelta, timezone

import jwt

from pymongo import MongoClient
from dotenv import load_dotenv

JWT_SECRET = "secret"
JWT_ALGORITHM = "HS256"
JWT_EXP_DELTA_SECONDS = 60




user = ns.model('User', { 
    'id': fields.Integer,
    'name': fields.String(required=True, min_length=1),
    'email': fields.String(required=True, min_length=5),
})

#create signup model
signup_model = auth_namespace.model(
    "SignUp", {
        "id": fields.Integer(),
        "username": fields.String(required=True),
        "email": fields.String(required=True),
        "password": fields.String(required=True),
    }
)

#create login model
login_model = auth_namespace.model(
    "Login", {
        "email": fields.String(required=True),
        "password": fields.String(required=True),
    }
)

def hash_password(password):
    hashed_password = jwt.encode({'password': password}, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return hashed_password

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
            "password": hash_password(data['password']),
        }
        
         # insert the user data into the MongoDB database
        try:
            collection = get_database()
            users = collection.find_one(
                {
                    "$or": [{"username": data["username"]},{"email":data["email"]}]
                }
            )
            if not users:
                collection.insert_one(new_user)
                return {"message": "User created successfully"}, 201
            else:
                
                return {"message": "User already exist"}, 403
        except:
            return {"message": "Error creating user"}, 500
        

@auth_namespace.route("/login")
class Login(Resource):
    @auth_namespace.expect(login_model)
    def post(self):
        """
        Logs user in and returns access token
        """
        data = request.get_json()
        
        email = data['email']
        password = data['password']
        
        # get the user with the given email
        collection = get_database()
        user = collection.find_one(
                {
                    "$or": [{email},{password}]
                }
            )
        if user is not None:
            #check if the password is correct
            hashed_password = hash_password(password)
            
            try:
                jwt.decode(hashed_password, JWT_SECRET, algorithms=['RS256'])
            except jwt.exceptions.DecodeError:
                return {"message": "Invalid password"}, 401
            
            # generate access token
            payload = {
            "sub": str(user["_id"]),
            "exp": datetime.utcnow() + timedelta(seconds = JWT_EXP_DELTA_SECONDS)
        }
        jwt_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
        return {"token": jwt_token}
    
    

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