#import libraries
import bcrypt
from flask import request
from flask_jwt_extended import (create_access_token, get_jwt_identity, jwt_required)
from flask_restx import Resource, fields


from sample_project.user import auth_namespace
from service import get_database

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
        
        email = data['email']
        username = data['username']

        # create a new user object
        new_user = {
            "username": username,
            "email": email,
            "password": bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
        }
        

        # insert the user data into the MongoDB database
        try:
            users_collection = get_database('users')
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
        users_collection = get_database('users')
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


@auth_namespace.route('/protected', methods=["GET"])
class Protected(Resource):
    @jwt_required()
    def get(self):
        #access identity of the current user with get_jwt_identity
        current_user = get_jwt_identity()
        return {"logged_in" : current_user}

