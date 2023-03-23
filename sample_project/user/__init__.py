from flask_restx import Namespace

ns = Namespace('User', path='/')
auth_namespace = Namespace('Auth', path='/')

from sample_project.user.v1 import views  # noqa
