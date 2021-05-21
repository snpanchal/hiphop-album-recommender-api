from flask import request
from flask_restx import Resource

from ..util.dto import AlbumDto
from ..service.album_service import get_albums, get_album, get_several_albums, search_album

api = AlbumDto.api
_album = AlbumDto.album

@api.route('/')
@api.doc(params={
    'page': {'description': 'page number', 'type': 'int', 'default': 1},
    'q': {'description': 'search query', 'type': 'string', 'default': ''},
    'ids': {'description': 'comma-separated list of album spotify ids', 'type': 'string', 'default': ''}
})
class AlbumList(Resource):
    @api.doc('get all albums paginated')
    @api.marshal_list_with(_album, envelope='albums')
    def get(self):
        album_ids = request.args.get('ids')
        if album_ids:
            return get_several_albums(album_ids.split(','))
        search_query = request.args.get('q')
        page = int(request.args.get('page'))
        res = search_album(search_query, page) if search_query else get_albums(page)
        return res.items


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
