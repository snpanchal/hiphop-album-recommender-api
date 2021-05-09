import pandas as pd
import numpy as np

from flask_restx import Resource, reqparse
from flask import request
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
from re import search

from ..util.dto import RecommendationsDto
from ..service.album_service import get_all_albums
from ..service.album_features_service import get_all_features

api = RecommendationsDto.api
_album = RecommendationsDto.album

@api.route('/')
class RecommendedAlbums(Resource):
    @api.doc('get recommended albums')
    @api.marshal_list_with(_album, envelope='albums')
    def post(self):
        album_ratings_json = request.get_json()
        album_ratings = pd.Series(album_ratings_json['ratings'])
        album_ratings = album_ratings.map(lambda rating: rating - 2.5)

        def filter_out_rated_albums(album):
            return album[0] not in album_ratings.index
        
        all_albums = get_all_albums()
        album_features = get_all_features()
        df_albums_info = pd.concat([pd.DataFrame([album.get_row()], columns=['spotify_id', 'name', 'artists']) for album in all_albums], ignore_index=True)
        df_albums_info.set_index('spotify_id', inplace=True)
        
        df_albums = pd.concat([pd.DataFrame([af.get_row()], columns=['spotify_id', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'valence', 'tempo']) for af in album_features], ignore_index=True)
        df_albums.set_index('spotify_id', inplace=True)

        df_album_artists = df_albums_info['artists'].str.get_dummies()
        df_albums = pd.concat([df_albums, df_album_artists], axis=1)

        cosine_sim = cosine_similarity(df_albums)
        min_similarity = cosine_sim.min()
        max_similarity = cosine_sim.max()
        scaled_similarity = (cosine_sim - min_similarity) / (max_similarity - min_similarity)

        df_correlation = pd.DataFrame(scaled_similarity, index=df_albums.index, columns=df_albums.index)
        for album_id in df_correlation:
            df_correlation.loc[album_id] = album_ratings[album_id] * df_correlation.loc[album_id] if album_id in album_ratings else 0

        album_scores = df_correlation.sum(axis=0)
        recommended_albums = []
        for album_id in album_scores.index:
            recommended_albums.append((album_id, album_scores[album_id]))
        recommended_albums = sorted(recommended_albums, key=lambda x: x[1], reverse=True)
        recommended_albums = list(filter(filter_out_rated_albums, recommended_albums))

        for album in recommended_albums[:20]:
            album_id = album[0]
            album_match = album[1]
            album_name = df_albums_info.loc[album_id]['name']
            album_artists = df_albums_info.loc[album_id]['artists']
            print('{} - {} (by {}), {}'.format(album_id, album_name, album_artists, album_match))
        
        return {'hello': request.get_json()}


# df_albums = pd.read_sql_query('SELECT * FROM albums', db_con)
# df_albums_info = df_albums[['spotify_id', 'name', 'artists']]
# df_albums_info.set_index('spotify_id', inplace=True)

# df_albums.drop(columns=['index', 'name', 'explicit'], inplace=True)
# df_albums.set_index('spotify_id', inplace=True)

# album_artists = df_albums['artists'].apply(replace_separators)
# df_albums.drop(columns='artists', inplace=True)

# df_album_artists = album_artists.str.get_dummies()
# df_albums = pd.concat([df_albums, df_album_artists], axis=1)

# test_ratings = pd.Series({
#     '41GuZcammIkupMPKH2OJ6I': 5.0,
#     '4yP0hdKOZPNshxUOjY0cZj': 3.0
# })
# test_ratings = test_ratings.map(lambda score: score - 2.5)

# cosine_sim = cosine_similarity(df_albums)
# min_similarity = cosine_sim.min()
# max_similarity = cosine_sim.max()
# scaled_similarity = (cosine_sim - min_similarity) / (max_similarity - min_similarity)

# df_correlation = pd.DataFrame(scaled_similarity, index=df_albums.index, columns=df_albums.index)
# for album_id in df_correlation:
#     df_correlation.loc[album_id] = test_ratings[album_id] * df_correlation.loc[album_id] if album_id in test_ratings else 0

# album_scores = df_correlation.sum(axis=0)
# recommended_albums = []
# for album_id in album_scores.index:
#     recommended_albums.append((album_id, album_scores[album_id]))
# recommended_albums = sorted(recommended_albums, key=lambda x: x[1], reverse=True)
# recommended_albums = list(filter(filter_out_rated_albums, recommended_albums))

# for album in recommended_albums[:20]:
#     album_id = album[0]
#     album_match = album[1]
#     album_name = df_albums_info.loc[album_id]['name']
#     album_artists = df_albums_info.loc[album_id]['artists']
#     print('{} - {} (by {}), {}'.format(album_id, album_name, album_artists, album_match))
