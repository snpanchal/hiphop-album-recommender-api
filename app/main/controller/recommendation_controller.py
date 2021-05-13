import pandas as pd
import os

from flask_restx import Resource
from flask import request
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy import create_engine

from ..util.dto import RecommendationsDto
from ..service.album_service import get_several_albums

api = RecommendationsDto.api
_album = RecommendationsDto.album

db_engine = create_engine(os.getenv('DATABASE_URL'))


@api.route('/')
class RecommendedAlbums(Resource):
    @api.doc('get recommended albums')
    @api.marshal_list_with(_album, envelope='data')
    def put(self):
        db_con = db_engine.connect()
        df_albums = pd.read_sql_table('similarity_matrix', db_con)
        df_albums.set_index('spotify_id', inplace=True)
        db_con.close()

        album_ratings_json = request.get_json()
        album_ratings = pd.Series(album_ratings_json['ratings'])
        album_ratings = album_ratings.map(lambda rating: rating - 2.5)

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
        
        recommended_album_details = get_several_albums([a[0] for a in recommended_albums])
        if not recommended_album_details:
            return []

        for i in range(len(recommended_album_details)):
            recommended_album_details[i].recommendation_score = album_scores[recommended_album_details[i].spotify_id]

        return recommended_album_details
