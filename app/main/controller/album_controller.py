from flask import request
from flask_restx import Resource

from ..util.dto import AlbumDto
from ..service.album_service import get_all_albums

api = AlbumDto.api
_album = AlbumDto.album


@api.route('/')
@api.response(404, 'Album not found')
class Album(Resource):
    @api.doc('get all albums')
    @api.marshal_with(_album)
    def get(self):
        albums = get_all_albums()
        if not albums:
            api.abort(404)
        else:
            return albums
