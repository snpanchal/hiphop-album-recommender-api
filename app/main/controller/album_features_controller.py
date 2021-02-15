from flask import request
from flask_restx import Resource

from ..util.dto import AlbumFeaturesDto
from ..service.album_features_service import get_features

api = AlbumFeaturesDto.api
_album_features = AlbumFeaturesDto.album_features


@api.route('/<spotify_id>')
@api.param('spotify_id', 'spotify id of album')
@api.response(404, 'Album features not found')
class AlbumFeatures(Resource):
    @api.doc('get album features')
    @api.marshal_with(_album_features)
    def get(self, spotify_id):
        album_features = get_features(spotify_id)
        if not album_features:
            api.abort(404)
        else:
            return album_features
