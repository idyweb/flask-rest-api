from flask import request, jsonify
from flask_restx import Resource, fields
from flask_jwt_extended import jwt_required


from sample_project.books import book_namespace
from service import get_database, get_books

book = book_namespace.model('Book', {
    'id': fields.Integer,
    'title': fields.String(required=True, min_length=1),
    'author': fields.String(required=True, min_length=5),
})

@book_namespace.route("/")
class BookList(Resource):
    @jwt_required()
    def get(self):
        books = get_books()
        return {"books": books}, 200
    
@book_namespace.route("/<string:title>")
class Book(Resource):
    @jwt_required()
    def get(self, title):
        books_collection = get_database('books')
        book = books_collection.find_one({"title": title})
        if book:
            book['_id'] = str(book['_id'])
            return {"book": book}, 200
        else:
            return {"message": "Book not found"}, 404
    
    
@book_namespace.route("/add")
class AddBook(Resource):
    @jwt_required()
    @book_namespace.expect(book)
    
    def post(self):
            data = request.get_json()
            
            #add a new book object
            new_book = {
                "title": data['title'],
                "author" :data['author']
            }
            title = data['title']
            
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
        

