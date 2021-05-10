from flask_restx import Resource

from ..util.dto import ArtistDto
from ..service.artist_service import get_all_artists, get_artist, search_artist

api = ArtistDto.api
_artist = ArtistDto.artist


@api.route('/')
class ArtistList(Resource):
    @api.doc('get all artists')
    @api.marshal_list_with(_artist, envelope='data')
    def get(self):
        return get_all_artists()

@api.route('/<artist_id>')
@api.param('artist_id', 'id of artist')
@api.response(404, 'Artist not found')
class Artist(Resource):
    @api.doc('get an artist')
    @api.marshal_with(_artist)
    def get(self, artist_id):
        artist = get_artist(artist_id)
        if not artist:
            api.abort(404)
        else:
            return artist

@api.route('/search/<search_query>')
@api.param('search_query', 'artist search query')
class ArtistSearch(Resource):
    @api.doc('search for an album')
    @api.marshal_list_with(_artist, envelope='artist_results')
    def get(self, search_query):
        if not search_query:
            return []
        return search_artist(search_query)
