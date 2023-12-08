import numpy as np
import pandas as pd
import sys
sys.path.append("..")
import high_level_input
import os
import subprocess

# for Novelty Metric
# assumes that the song name or artist name does not contain the underscore (_)
def filtering_artist_names(df):
    #print(df)
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
    #artist_condition, name_condition
    #print(f"artist_name {artist_condition}, name_condition{name_condition}")
    found_row = df[df['artists'].apply(lambda x: any(artist in x for artist in artist_condition.split())) & (df['name'] == name_condition)]
    #print(found_row)
    found_key = found_row['key'].values[0]
    return found_key


def find_recommended_keys(df, concat_df):
    recommended_keys = []
    recomended_song_list = list(df['All_songs'].values)
    i=0
    for song in recomended_song_list:
        
        #print(i)
        i+=1
        found_key = find_key(concat_df, song)
        recommended_keys.append(found_key)
    return recommended_keys


# Diversity Metric
def calculate_diversity(recommended_keys):
    total_occurrences = sum(recommended_keys)
    key_probabilities = np.array(recommended_keys) / total_occurrences
    probabilities = key_probabilities / np.sum(key_probabilities)
     # Exclude zero probabilities to avoid NaN in log
    non_zero_probabilities = probabilities[probabilities > 0]
    
    # Calculate entropy using the formula
    entropy = -np.sum(non_zero_probabilities * np.log2(non_zero_probabilities))
    
    return entropy


# topN agreement Metric
def topN_agreement(prediction_df, gt_rank_df, alpha = 0.5 ** (1/3)):
    seed_song_names = set(list(prediction_df['Seed_song_names']))
    
    topN_scores = []
    for seed_song in seed_song_names:
        print(seed_song)
        sorted_prediction = prediction_df[prediction_df['Seed_song_names'] == seed_song]

        sorted_prediction = sorted_prediction.set_index('All_songs')['Rank'].to_dict()
        print(sorted_prediction)
        sorted_gt = gt_rank_df[gt_rank_df['Seed_song_names'] == seed_song]
        print(f"SORTED GT: {sorted_gt}")
        sorted_gt = sorted_gt.set_index('All_songs')['Rank'].to_dict()
        print(f"SORTED GT: {sorted_gt}")
        result = 0
        for algo_song, algo_rank in sorted_prediction.items():
            alpha_for_c = alpha ** 2  
            alpha_c = alpha_for_c ** (algo_rank - 1)   
            print(f"Sorted GT: {sorted_gt.keys()}")
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
def main_metric(prediction_df, gt_df, counter):
    # predict_df = pd.read_csv('prediction.csv')
    # gt_df = pd.read_csv('ground_truth.csv')  
    
    # Novelty metrics
    user_artist_names, predicted_artist_names = filtering_artist_names(prediction_df)
    novelty = calculate_novelty(user_artist_names, predicted_artist_names)
    print(f"Novelty Score: {novelty}")
    
    # Entropy metrics 

    if counter == 0:
        working_directory = "../"
        os.chdir(working_directory)
        subprocess.run(["python3", "high_level_input.py"])
        
    else:
        working_directory="./"
        os.chdir(working_directory)
        subprocess.run(["python3", "high_level_input.py"])
    print(os.getcwd())
    concat_df = high_level_input.add_user_songs_if_not_exists()
    print(len(concat_df))
    recommended_keys = find_recommended_keys(prediction_df, concat_df)
    entropy = calculate_diversity(recommended_keys)
    print(f"Entropy: {entropy}")
    
    # # topN agreement Metric     
    # topN_score = topN_agreement(prediction_df, gt_df)
    
# if __name__ == "__main__":
    
#     main()
