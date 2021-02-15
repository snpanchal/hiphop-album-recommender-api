# app/__init__.py

from flask_restx import Api
from flask import Blueprint

# REPLACE NAMESPACES
from .main.controller.album_controller import api as album_ns
from .main.controller.album_features_controller import api as album_features_ns

blueprint = Blueprint('api', __name__)

api = Api(
    blueprint,
    title='Recommender API',
    version='1.0',
    description='a boilerplate for flask restplus web service'
)

api.add_namespace(album_ns, path='/albums')
api.add_namespace(album_features_ns, path='/album_features')
