from flask import request
from flask_restx import Resource, fields
from flask_login import login_required, current_user
from sample_project.books import ns
from sample_project.user.v1.service import get_database

book = ns.model('Book', {
    'id': fields.Integer,
    'title': fields.String(required=True, min_length=1),
    'author': fields.String(required=True, min_length=5),
})

@ns.route("books/add", methods=['GET','POST'])
@login_required
def add_book():
    if request.method == 'POST':
        data = request.get_json()
        
        #add a new book object
        new_book = {
            "title": data['title'],
            "author":data['author']
        }
        title = data['title']
        author = data['author']
        
        #add book into database
        try:
            books_collection = get_database()
            book = books_collection.find_one({"title":title})
            
            if not book:
                books_collection.insert_one(new_book)
                return {"message": "Book added successfully"}, 201
            else:
                return {"message": "Book already exist"}, 403
        except Exception as e:
            return {"message": f"Error adding book: {str(e)}"}, 500
    

