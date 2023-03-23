from flask_restx import Resource, fields,Namespace,Api 
from flask import request
import bcrypt

from sample_project.user import ns, auth_namespace
from sample_project.user.v1.service import get_database

import json
from datetime import datetime, timedelta, timezone

import jwt
from jwt import (JWT, jwk_from_dict, jwk_from_pem,)
from jwt.utils import get_int_from_datetime

instance = JWT()
# create signup model
signup_model = auth_namespace.model(
    "SignUp", {
        "id": fields.Integer(),
        "username": fields.String(required=True),
        "email": fields.String(required=True),
        "password": fields.String(required=True),
    }
)

def hash_password(password):
    signing_key = jwk_from_dict(
            {
    "kty": "RSA",
    "n":"0vx7agoebGcQSuuPiLJXZptN9nndrQmbXEps2aiAFbWhM78LhWx4cbbfAAtVT86zwu1RK7aPFFxuhDR1L6tSoc_BJECPebWKRXjBZCiFV4n3oknjhMstn64tZ_2W-5JsGY4Hc5n9yBXArwl93lqt7_RN5w6Cf0h4QyQ5v-65YGjQR0_FDW2QvzqY368QQMicAtaSqzs8KJZgnYb9c7d0zgdAZHzu6qMQvRL5hajrn1n91CbOpbISD08qNLyrdkt-bFTWhAI4vMQFh6WeZu0fM4lFd2NcRwr3XPksINHaQ-G_xBniIqbw0Ls1jF44-csFCur-kEgU8awapJzKnqDKgw",
    "d":"X4cTteJY_gn4FYPsXB8rdXix5vwsg1FLN5E3EaG6RJoVH-HLLKD9M7dx5oo7GURknchnrRweUkC7hT5fJLM0WbFAKNLWY2vv7B6NqXSzUvxT0_YSfqijwp3RTzlBaCxWp4doFk5N2o8Gy_nHNKroADIkJ46pRUohsXywbReAdYaMwFs9tv8d_cPVY3i07a3t8MN6TNwm0dSawm9v47UiCl3Sk5ZiG7xojPLu4sbg1U2jx4IBTNBznbJSzFHK66jT8bgkuqsk0GjskDJk19Z4qwjwbsnn4j2WBii3RL-Us2lGVkY8fkFzme1z0HbIkfz0Y6mqnOYtqc0X4jfcKoAC8Q",
    "e": "AQAB"}
        )
    hashed_password = instance.encode({'password': password}, signing_key, alg='RS256')
    return hashed_password


@auth_namespace.route("/signup")
class Auth(Resource):
    @auth_namespace.expect(signup_model)
    def post(self):
        
        """
        create a new user account
        """ 
        data = request.get_json()

        # hash the password using bcrypt
        
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

# create signup model
signin_model = auth_namespace.model(
    "SignIn", {
        "email": fields.String(required=True),
        "password": fields.String(required=True),
    }
)

@auth_namespace.route("/login")
class Auth(Resource):
    @auth_namespace.expect(signin_model)
    def post(self):
        """
        authenticate user
        """ 
        data = request.get_json()
        
        #find the user in the MongoDB database
        try:
            collection = get_database()
            users = collection.find_one(
                {
                    "$or": [{"username": data["username"]},{"email":data["email"]}]
                }
            )
            
            #check if user exist and the password matches
            if user and bcrypt.checkpw(data["password"].encode("utf-8"), user["password"].encode("utf-8")):
                return {"message": "Authenticated successfully"}, 200
            else:
                return {"message": "Invalid email or password"}, 401
        except Exception as reason:
            return {"message":f"Error authenticating user{reason}"}, 500



user = ns.model('User', { 
    'id': fields.Integer,
    'name': fields.String(required=True, min_length=1),
    'email': fields.String(required=True, min_length=5),
})


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
