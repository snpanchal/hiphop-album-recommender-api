from flask_restx import Namespace, fields

class AlbumDto:
    api = Namespace('album', description='album related operations')
    artist = api.model('artist', {
        'id': fields.Integer(required=True, description='album id'),
        'name': fields.String(required=True, description='artist name')
    })
    album = api.model('album', {
        'spotify_id': fields.String(required=True, description='album spotify id'),
        'name': fields.String(required=True, description='album title'),
        'image_link': fields.String(required=True, description='album image link'),
        'artists': fields.List(fields.Nested(artist))
    })

class AlbumFeaturesDto:
    api = Namespace('album_features', description='album features related operations')
    album_features = api.model('album_features', {
        'spotify_id': fields.String(required=True, description='album spotify id'),
        'explicit': fields.Integer(required=True, description='album explicit'),
        'acousticness': fields.Float(required=True, description='album acousticness'),
        'danceability': fields.Float(required=True, description='album danceability'),
        'energy': fields.Float(required=True, description='album energy'),
        'instrumentalness': fields.Float(required=True, description='album instrumentalness'),
        'liveness': fields.Float(required=True, description='album liveness'),
        'loudness': fields.Float(required=True, description='album loudness'),
        'speechiness': fields.Float(required=True, description='album speechiness'),
        'valence': fields.Float(required=True, description='album valence'),
        'tempo': fields.Float(required=True, description='album tempo'),
    })

class ArtistDto:
    api = Namespace('artist', description='artist related operations')
    album = api.model('album', {
        'spotify_id': fields.String(required=True, description='album spotify id'),
        'name': fields.String(required=True, description='album title'),
        'image_link': fields.String(required=True, description='album image link')
    })
    artist = api.model('artist', {
        'id': fields.Integer(required=True, description='artist id'),
        'name': fields.String(required=True, description='artist name'),
        'albums': fields.List(fields.Nested(album))
    })

class RecommendationsDto:
    api = Namespace('recommendations', description='album recommendations operations')
    artist = api.model('artist', {
        'id': fields.Integer(required=True, description='album id'),
        'name': fields.String(required=True, description='artist name')
    })
    album = api.model('album', {
        'spotify_id': fields.String(required=True, description='album spotify id'),
        'name': fields.String(required=True, description='album title'),
        'recommendation_score': fields.Float(required=True, description='album recommendation score'),
        'artists': fields.List(fields.Nested(artist))
    })