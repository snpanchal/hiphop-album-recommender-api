from app.main import db
from app.main.models import Album

def get_all_albums():
    return Album.query.all()

def get_album(spotify_id):
    return Album.query.filter_by(spotify_id=spotify_id).first()
