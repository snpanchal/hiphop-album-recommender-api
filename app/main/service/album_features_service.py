from app.main import db
from app.main.model.album_features import AlbumFeatures


def get_features(spotify_id):
    return AlbumFeatures.query.filter_by(spotify_id=spotify_id).first()
