import numpy as np
import pandas as pd

# for Novelty Metric
# assumes that the song name or artist name does not contain the underscore (_)
def filtering_artist_names(df):
    user_song_names = list(df['Seed_song_names'])
    predicted_song_names = list(df['All_songs'])

    user_artist_names = [x.split('_')[0] for x in user_song_names] # user_artists
    predicted_artist_names = [x.split('_')[0] for x in predicted_song_names] # recommended_artists
    return user_artist_names, predicted_artist_names


# Novelty Metric
def calculate_novelty(user_artists, recommended_artists):
    novelty = len(set(recommended_artists) - set(user_artists)) / len(set(recommended_artists))
    return novelty


# For Diversity Metric
def find_key(df, sample):
    artist_condition, name_condition = sample.split('_')
    name_condition = name_condition.replace('.mp3', '')
    artist_condition, name_condition
    found_row = df[df['artists'].apply(lambda x: artist_condition in x) & (df['name'] == name_condition)]
    found_key = found_row['key'].values[0]
    return found_key


def find_recommended_keys(df):
    recommended_keys = []
    recomended_song_list = list(df['All_songs'].values)
    for song in recomended_song_list:
        found_key = find_key(df, song)
        recommended_keys.append(found_key)
    return recommended_keys


# Diversity Metric
def calculate_diversity(recommended_keys):
    genre_histogram = np.bincount(recommended_keys)
    entropy = -np.sum((genre_histogram / len(recommended_keys)) * np.log(genre_histogram / len(recommended_keys)))
    return entropy


# topN agreement Metric
def topN_agreement(prediction_df, gt_rank_df, alpha = 0.5 ** (1/3)):
    seed_song_names = set(list(prediction_df['Seed_song_names']))
    
    topN_scores = []
    for seed_song in seed_song_names:
        sorted_prediction = prediction_df[prediction_df['Seed_song_names'] == seed_song]
        sorted_prediction = sorted_prediction.set_index('All_songs')['Rank'].to_dict()
        
        sorted_gt = gt_rank_df[gt_rank_df['Seed_song_names'] == seed_song]
        sorted_gt = sorted_gt.set_index('Recommended_song_names')['Rank'].to_dict()
        
        result = 0
        for algo_song, algo_rank in sorted_prediction.items():
            alpha_for_c = alpha ** 2  
            alpha_c = alpha_for_c ** (algo_rank - 1)   
            
            gt_rank = sorted_gt[algo_song]
            alpha_r = alpha ** (gt_rank - 1)
            result += alpha_r * alpha_c 
                   
        topN_scores.append(result)
    
    N = len(topN_scores)
    normalized_scores = [s_i / max(topN_scores) for s_i in topN_scores]
    overall_score = (1 / N) * sum(normalized_scores)
    print(f"topN agreement: {overall_score}")
    return overall_score


# Run three metrics for the generated playlist
def main():
    predict_df = pd.read_csv('prediction.csv')
    gt_df = pd.read_csv('ground_truth.csv')  
    
    # Novelty metrics
    user_artist_names, predicted_artist_names = filtering_artist_names(predict_df)
    novelty = calculate_novelty(user_artist_names, predicted_artist_names)
    print(f"Novelty Score: {novelty}")
    
    # Entropy metrics 
    recommended_keys = find_recommended_keys(predict_df)
    entropy = calculate_diversity(recommended_keys)
    print(f"Entropy: {entropy}")
    
    # topN agreement Metric     
    topN_score = topN_agreement(predict_df, gt_df)
    
main()
