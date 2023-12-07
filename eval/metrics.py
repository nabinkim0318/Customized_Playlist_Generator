import numpy as np
from sklearn.metrics import ndcg_score


# RMSE Calculation
def rmse(predictions, targets):
    return np.sqrt(((predictions - targets) ** 2).mean())


# NDCG Calculation
def calculate_ndcg(y_true, y_score, k=10):
    return ndcg_score([y_true], [y_score], k=k)


# Novelty Metric
def calculate_novelty(recommended_artists, user_artists):
    novelty = len(set(recommended_artists) - set(user_artists)) / len(set(recommended_artists))
    return novelty


# Diversity Metric
def calculate_diversity(recommended_genres):
    genre_histogram = np.bincount(recommended_genres)
    entropy = -np.sum((genre_histogram / len(recommended_genres)) * np.log(genre_histogram / len(recommended_genres)))
    return entropy


# Freshnss Metric
def calculate_freshness(recommended_song_dates):
    current_time = max(recommended_song_dates)
    freshness = np.mean(current_time - np.array(recommended_song_dates))
    return freshness


# Popularity Metric
def calculate_popularity(song_popularity, top_n_songs):
    popularity = np.mean([song_popularity[song] for song in top_n_songs])
    return popularity
