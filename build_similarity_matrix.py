import pandas as pd
import psycopg2
import os

from sqlalchemy import create_engine

from app.main.service.album_service import get_all_albums
from app.main.service.album_features_service import get_all_features
from manage import app

db_engine = create_engine(os.getenv('DATABASE_URL'))

with app.app_context():
    db_con = db_engine.connect()
    all_albums = get_all_albums()
    album_features = get_all_features()
    df_albums_info = pd.concat([pd.DataFrame([album.get_row()], columns=['spotify_id', 'name', 'artists']) for album in all_albums], ignore_index=True)
    df_albums_info.set_index('spotify_id', inplace=True)

    df_albums = pd.concat([pd.DataFrame([af.get_row()], columns=['spotify_id', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'valence', 'tempo']) for af in album_features], ignore_index=True)
    df_albums.set_index('spotify_id', inplace=True)

    df_album_artists = df_albums_info['artists'].str.get_dummies()
    df_albums = pd.concat([df_albums, df_album_artists], axis=1)

    df_albums.to_sql('similarity_matrix', db_con, if_exists='replace')

    db_con.close()