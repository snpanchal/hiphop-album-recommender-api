import pandas as pd
import numpy as np

from flask_restx import Resource, reqparse
from flask import request
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
from re import search

from ..util.dto import RecommendationsDto
from ..service.album_service import get_all_albums, get_albums_list
from ..service.album_features_service import get_all_features

api = RecommendationsDto.api
_album = RecommendationsDto.album

@api.route('/')
class RecommendedAlbums(Resource):
    @api.doc('get recommended albums')
    @api.marshal_list_with(_album, envelope='recommended_albums')
    def post(self):
        album_ratings_json = request.get_json()
        album_ratings = pd.Series(album_ratings_json['ratings'])
        album_ratings = album_ratings.map(lambda rating: rating - 2.5)
        
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

        def filter_out_rated_albums(album):
            return album[0] not in album_ratings.index

        album_scores = df_correlation.sum(axis=0)
        recommended_albums = [(album_id, album_scores[album_id]) for album_id in album_scores.index]
        recommended_albums = list(filter(filter_out_rated_albums, recommended_albums))
        recommended_albums = sorted(recommended_albums, key=lambda x: x[1], reverse=True)[:15]
        
        recommended_album_details = get_albums_list([a[0] for a in recommended_albums])
        for i in range(len(recommended_album_details)):
            recommended_album_details[i].recommendation_score = album_scores[recommended_album_details[i].spotify_id]

        return recommended_album_details
