from .. import db, flask_bcrypt
from sqlalchemy.orm import relationship


class AlbumFeatures(db.Model):
    __tablename__ = 'album_features'

    spotify_id = db.Column(db.String(255), primary_key=True)
    explicit = db.Column(db.Boolean)
    acousticness = db.Column(db.Float)
    danceability = db.Column(db.Float)
    energy = db.Column(db.Float)
    instrumentalness = db.Column(db.Float)
    liveness = db.Column(db.Float)
    loudness = db.Column(db.Float)
    speechiness = db.Column(db.Float)
    valence = db.Column(db.Float)
    tempo = db.Column(db.Float)
