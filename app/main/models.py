from . import db

album_artists = db.Table('album_artists',
    db.Column('album_id', db.String(22), db.ForeignKey('albums.spotify_id'), primary_key=True),
    db.Column('artist_id', db.Integer, db.ForeignKey('artists.id'), primary_key=True)
)

class Album(db.Model):
    __tablename__ = 'albums'
    
    spotify_id = db.Column(db.String(22), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    image_link = db.Column(db.String(255), nullable=True)
    artists = db.relationship('Artist', secondary=album_artists, backref='albums', lazy=True)

    def get_row(self):
        artists_str = '|'.join([a.name for a in self.artists])
        return [self.spotify_id, self.name, artists_str]

class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

class AlbumFeatures(db.Model):
    __tablename__ = 'album_features'

    spotify_id = db.Column(db.String(22), db.ForeignKey('albums.spotify_id'), primary_key=True)
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

    def get_row(self):
        return [self.spotify_id, self.acousticness, self.danceability, self.energy, self.instrumentalness, self.liveness, self.loudness, self.speechiness, self.valence, self.tempo]
