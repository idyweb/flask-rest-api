from flask_restx import Namespace

#ns = Namespace('Book', path='/')
book_namespace = Namespace('Book', path='/')


from sample_project.books.v1 import views  # noqa