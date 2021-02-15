from .. import db, flask_bcrypt
from sqlalchemy.orm import relationship


class Album(db.Model):
    __tablename__ = 'albums'

    spotify_id = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    artists = db.Column(db.String(255), nullable=False)
