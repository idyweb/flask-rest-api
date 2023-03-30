from pymongo import MongoClient
from decouple import config



# Load environment variables from .env file

# connect with MongoDB
def get_database(collection_name):
    # Load environment variables from .env file

    # connect with MongoDB
    CONNECTION_STRING = config("CONNECTION_STRING")
    client = MongoClient(CONNECTION_STRING)
    
    #create the database
    dbname = client['bookstore']
    #create collections for user
    collection = dbname[collection_name]
    return collection


def get_books():
    #get books collection
    books_collection = get_database('books')
    
    #find all books and conver _id to string
    books = list(books_collection.find())
    for book in books:
        book['_id'] = str(book['_id'])
    return books 