from flask_restx import Resource

from ..util.dto import AlbumDto
from ..service.album_service import get_all_albums, get_album

api = AlbumDto.api
_album = AlbumDto.album


@api.route('/')
class AlbumList(Resource):
    @api.doc('get all albums')
    @api.marshal_list_with(_album, envelope='data')
    def get(self):
        return get_all_albums()


@api.route('/<spotify_id>')
@api.param('spotify_id', 'spotify id of album')
@api.response(404, 'Album not found')
class Album(Resource):
    @api.doc('get an album')
    @api.marshal_with(_album)
    def get(self, spotify_id):
        album = get_album(spotify_id)
        if not album:
            api.abort(404)
        else:
            return album
