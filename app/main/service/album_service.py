from sqlalchemy import func

from app.main import db
from app.main.models import Album

def get_all_albums():
    return Album.query.all()

def get_albums(page_num):
    return Album.query.paginate(per_page=50, page=page_num, error_out=False)

def get_album(album_id):
    return Album.query.filter_by(spotify_id=album_id).first()

def get_several_albums(album_ids):
    if len(album_ids) > 0:
        return Album.query.filter(Album.spotify_id.in_(album_ids)).all()

def search_album(search_query):
    return Album.query.filter(Album.name.ilike(f'%{search_query}%')).all()
