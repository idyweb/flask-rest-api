from flask import request
from flask_restx import Resource, fields
from flask_login import login_required, current_user
from flask_jwt_extended import (JWTManager, create_access_token, get_jwt_identity, jwt_required)
from sample_project.books import book_namespace
from service import get_database

book = book_namespace.model('Book', {
    'id': fields.Integer,
    'title': fields.String(required=True, min_length=1),
    'author': fields.String(required=True, min_length=5),
})

@book_namespace.route("/add")
class Book(Resource):
    @jwt_required()
    @book_namespace.expect(book)
    def post(self):
            data = request.get_json()
            title = data['title']
            author = data['author']
            
            #add a new book object
            new_book = {
                "title": title,
                "author" : author
            }
            #add book into database
            try:
                books_collection = get_database('books')
                book = books_collection.find_one({"title":title})
                
                if not book:
                    books_collection.insert_one(new_book)
                    return {"message": "Book added successfully"}, 201
                else:
                    return {"message": "Book already exist"}, 403
            except Exception as e:
                return {"message": f"Error adding book: {str(e)}"}, 500
        

