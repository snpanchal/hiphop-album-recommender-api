from app.main import db
from app.main.models import AlbumFeatures

def get_all_features():
    return AlbumFeatures.query.all()

def get_features(spotify_id):
    return AlbumFeatures.query.filter_by(spotify_id=spotify_id).first()
