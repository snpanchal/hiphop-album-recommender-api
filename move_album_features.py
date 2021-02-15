import pandas as pd
import sqlite3

db_con = sqlite3.connect('app/main/albums.db')

df_albums = pd.read_sql_query('SELECT * FROM album_info', db_con)

# --- Collect album info into new table album_info ---
# df_albums_info = df_albums[['spotify_id', 'name', 'artists']]
# df_albums_info.set_index('spotify_id', inplace=True)
# df_albums_info.to_sql('album_info', db_con, if_exists='replace')

# --- Collect album features into new table album_features ---
# df_albums = df_albums[[
#     'spotify_id', 'explicit', 'acousticness', 'danceability', 'energy', 'instrumentalness',
#     'liveness', 'loudness', 'speechiness', 'valence', 'tempo'
# ]]
# df_albums.set_index('spotify_id', inplace=True)
# df_albums.to_sql('album_features', db_con, if_exists='replace')

# --- Move data from album_info to albums table ---
df_albums.set_index('spotify_id', inplace=True)
df_albums.to_sql('albums', db_con, if_exists='replace')

db_con.close()
