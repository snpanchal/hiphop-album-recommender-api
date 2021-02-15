from flask_restx import Namespace, fields


class AlbumDto:
    api = Namespace('album', description='album related operations')
    album = api.model('album', {
        'spotify_id': fields.String(required=True, description='album spotify id'),
        'name': fields.String(required=True, description='album title'),
        'artists': fields.String(required=True, description='album artists')
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
