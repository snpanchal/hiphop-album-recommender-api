from app.main import db
from app.main.model.album import Album


def get_all_albums():
    return Album.query.filter_by(artists='Logic').limit(10).all()
