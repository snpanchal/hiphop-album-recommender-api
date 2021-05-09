from flask_restx import Api
from flask import Blueprint

from .main.controller.album_controller import api as album_ns
from .main.controller.album_features_controller import api as album_features_ns
from .main.controller.artist_controller import api as artist_ns
from .main.controller.recommendation_controller import api as recommendation_ns

blueprint = Blueprint('api', __name__)

api = Api(
    blueprint,
    title='Recommender API',
    version='1.0',
    description='a boilerplate for flask restplus web service'
)

api.add_namespace(album_ns, path='/albums')
api.add_namespace(album_features_ns, path='/album_features')
api.add_namespace(artist_ns, path='/artists')
api.add_namespace(recommendation_ns, path='/recommend')
