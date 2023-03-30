from flask import Blueprint, current_app
from flask_restx import Api

from sample_project.user import ns as ns_user
from sample_project.person import ns as ns_person
from sample_project.user import auth_namespace as ns_auth
from sample_project.books import ns as ns_book


blueprint = Blueprint('api_1_0', __name__)


api = Api(
    blueprint,
    doc=current_app.config['API_DOCS_URL'],
    catch_all_404s=True
)
api.namespaces.clear()
api.add_namespace(ns_user)
api.add_namespace(ns_person)
api.add_namespace(ns_auth,path='/auth')
api.add_namespace(ns_book,path='/book')
