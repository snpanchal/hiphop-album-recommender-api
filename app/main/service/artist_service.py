from sqlalchemy import func

from app.main import db
from app.main.models import Artist

def get_all_artists():
    return Artist.query.limit(30).all()

def get_artist(artist_id):
    return Artist.query.filter_by(id=artist_id).first()

def search_artist(search_query):
    return Artist.query.filter(Artist.name.ilike(f'%{search_query}%')).all()
