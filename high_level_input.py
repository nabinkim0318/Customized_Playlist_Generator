
# basic libraries 
import os
import pandas as pd
import numpy as np
import string
import random
import shutil

# Spotify API calls 
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Cosine similarity 
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
import pandas as pd

import config
import get_user_top_items

TERM = config.TERM


def add_user_songs_if_not_exists(term=TERM):
    df1 = pd.read_csv(f'./user_top_items/top_tracks_{term}.csv')
    df2 = pd.read_csv("tracks_features.csv")
    concat_df = pd.concat([df1, df2], axis=0)
    concat_df = concat_df.drop_duplicates(subset=["id"])
    
    return concat_df
    


# The list of Spotify IDs
def get_seed_songs(df):    
    top_20 = df.head(20)
    filtered_years = top_20[top_20['year'] <= 2020]
    seed_songs_list = filtered_years['id'].tolist()[:10] 
    print(f"seed_songs_list: {seed_songs_list}")
    
    return seed_songs_list


# get each song's release year 
def get_years_from_spotify_ids(df, seed_songs_list):
    years_list = []
    for spotify_id in seed_songs_list:
        filtered_row = df[df['id'] == spotify_id]
        if not filtered_row.empty: 
            matching_year = filtered_row.iloc[0]['year']
            years_list.append(matching_year)
        else:
            print(f"No match found for Spotify ID: {spotify_id}")
    print(f"years_list: {years_list}")
    return years_list


def get_sub_df_dict(df, years_list):
    if not years_list:
        # Handle the case where years_list is None or empty
        print("Error: years_list is None or empty.")
        return {}

    sub_df_dict = {}
    
    for year in years_list:
        sub_df = df[df['year'] == year]
        sub_df_dict[year] = sub_df
    return sub_df_dict

# find top 10 songs per seed song, drop the top 10 songs of sub_df if two 
# or more seed songs are from the same year
def find_similar_songs(df, sub_df_dict, song_id):
    # get year_specific_df based on song_id
    #df = df.iloc[40:]
    year = df.loc[df['id'] == song_id, "year"].values[0]
 
    print(f"len(sub_df_dict: {len(sub_df_dict)}")
    sub_df = sub_df_dict[year]

    print(f"len(sub_df: {len(sub_df)}")
    
    sub_df.reset_index(drop=True, inplace=True)
    
    # filter numerical, key and id columns 
    numerical_columns = ['danceability', 'energy', 'loudness', 'mode', 'speechiness', 'acousticness',
                            'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms', 'time_signature']
    data = sub_df[['id'] + numerical_columns + ['key']]  
    scaler = StandardScaler()
    normalized_data = scaler.fit_transform(data[numerical_columns])

    # Combine normalized data, one-hot encoded 'key' column, and spotify_id
    encoded_key = pd.get_dummies(data['key'], prefix='key')
    combined_data = pd.concat([pd.DataFrame(normalized_data, columns=numerical_columns), encoded_key], axis=1)
    data_with_encoded_key = pd.concat([data[['id']], combined_data], axis=1)
    data_with_encoded_key.reset_index(drop=True, inplace=True)
    print("encoded")
    # print(len(data_with_encoded_key))

    # Calculate cosine similarity matrix after dropping the song_to_compare
    song_to_compare = data_with_encoded_key[data_with_encoded_key['id'] == song_id]
    df_without_seed = data_with_encoded_key.drop(song_to_compare.index)
    song_to_compare = song_to_compare.drop('id', axis = 1)
    df_without_seed = df_without_seed.drop('id', axis = 1)
    # print(f"song_to_compare: {song_to_compare}")
    # print(f"df_without_seed: {df_without_seed}")

    # Getting the top 10 most similar songs
    cosine_sim = cosine_similarity(song_to_compare, df_without_seed)
    similarity_scores = list(enumerate(cosine_sim[0]))
   # print(f"len(similarity_scores): {similarity_scores}")
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)[1:101]
    top_100_indices = [i[0] for i in similarity_scores]
    top_100_songs = sub_df.iloc[top_100_indices]
    
    # update sub_df_dict 
    sub_df = sub_df[~sub_df['id'].isin(top_100_songs['id'])]
    sub_df_dict[year] = sub_df

    # Set the index of top_100_songs to the original index of sub_df_2014
    top_100_songs.reset_index(drop=True, inplace=True)
    top_100_songs_id = list(top_100_songs['id'])
    print(f"seed_song: {song_id}")
    print(len(top_100_songs_id))
    return sub_df_dict, top_100_songs_id

def get_preview_url(spotify_id):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id="0c8dbb1cfb78479d9613930fbc9ad872",
        client_secret="260a210533424c4592cb3d24d1da7b85",
        redirect_uri="https://www.audiocontentanalysis.org",
        scope="user-top-read",
    ))
    track = sp.track(spotify_id)
    url = track['preview_url']
    return spotify_id, url

def clean_file_name(name):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    cleaned_name = ''.join(c for c in name if c in valid_chars)
    return cleaned_name

def get_preview_audio(df, spotify_id, url, seed_song, seed_song_id = None):
    if url:
        response = requests.get(url)
        if response.status_code == 200:
            filtered_row = df[df['id'] == spotify_id]
            if not filtered_row.empty:
                artist_names = filtered_row['artists'].values[0]
                song_name = filtered_row['name'].values[0]

                file_name = clean_file_name(artist_names) + '_' + clean_file_name(song_name)
                file_name += '.mp3'  # Add file extension

                os.makedirs('./audio/seed_songs', exist_ok=True)
                os.makedirs('./audio/input/similarity_based', exist_ok=True)

                if not seed_song:
                    filtered_row_seed = df[df['id'] == seed_song_id]
                    if not filtered_row_seed.empty:
                        artist_names_seed = filtered_row_seed['artists'].values[0]
                        song_name_seed = filtered_row_seed['name'].values[0]

                        seed_song_folder_name = clean_file_name(artist_names_seed) + '_' + clean_file_name(song_name_seed)
                        seed_song_folder_path = os.path.join('./audio/input/similarity_based', seed_song_folder_name)
                        os.makedirs(seed_song_folder_path, exist_ok=True)

                        file_path = os.path.join(seed_song_folder_path, file_name)
                        with open(file_path, 'wb') as f:
                            f.write(response.content)
                else:
                    file_path = os.path.join('./audio/seed_songs', file_name)
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
        else:
            print(f"{spotify_id} preview is not available")
            return spotify_id
    else:
        print(f"spotify api cannot find preview url for {spotify_id}")
        return spotify_id


def get_preview_audio_from_list(df, spotify_id_list, seed_song, seed_song_id=None):
    no_preview_spotify_id_list = []
    count = 0  
    
    for spotify_id in spotify_id_list:
        if count >= 10: 
            break
        
        spotify_id, url = get_preview_url(spotify_id)
        result = get_preview_audio(df, spotify_id, url, seed_song, seed_song_id if not seed_song else None)
        
        if not result:
            no_preview_spotify_id_list.append(spotify_id)
            count += 1  
    print(f"no_preview_spotify_id_list: {no_preview_spotify_id_list}")

def find_and_download_seed_songs(df, top_items_list):
    actual_seed_list = []
    count = 0
    for top_item_id in top_items_list:
        if count >= 5:
            break  
        spotify_id, url = get_preview_url(top_item_id)
        result = get_preview_audio(df, top_item_id, url, True)
        if not result:
            count += 1
            actual_seed_list.append(spotify_id)
            print(f"count: {count}")      
    return actual_seed_list

def get_recommendation_pool(df):
    # get seed songs from user's top tracks
    seed_songs_list = get_seed_songs(df) # This now gets the user's top tracks

    # get years based on seed songs
    years_list = get_years_from_spotify_ids(df, seed_songs_list)
    
    # set sub_df for each seed song's year 
    sub_df_dict = get_sub_df_dict(df, years_list)
    
    # get audio for each seed song in the seed_songs folder --> need to be changed
    actual_seed_list = find_and_download_seed_songs(df, seed_songs_list)
    
    # get audio and ID of top 100 songs per seed song 
    for seed_song_id in actual_seed_list: 
        sub_df_dict, top_100_songs_id = find_similar_songs(df, sub_df_dict, seed_song_id)
        get_preview_audio_from_list(df, top_100_songs_id, False, seed_song_id)
        #print(sub_df_dict, top_100_songs_id)

def similarity_based_main():
    #get_user_top_items.print_top_items()
    get_recommendation_pool(add_user_songs_if_not_exists(term=TERM)) # it should creates a seed_song folder and the corresponding top_10 per seed song





# %%
"""
### Approach 2: Randomly select 50 songs
"""

# %%
def create_directories():
    seed_song_list = os.listdir('./audio/seed_songs')
    for folder_name in seed_song_list:
        folder_path = os.path.join('random_songs', folder_name)
        os.makedirs(folder_path, exist_ok=True)
        
# using spotify API to get the preview url 
def get_preview_url(spotify_id):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id="0c8dbb1cfb78479d9613930fbc9ad872",
        client_secret="260a210533424c4592cb3d24d1da7b85",
        redirect_uri="https://www.audiocontentanalysis.org",
        scope="user-top-read",
    ))
    track = sp.track(spotify_id)
    url = track['preview_url']
    return spotify_id, url

# download the audio in the correct directory 
def get_preview_random_audio(df, spotify_id, url):
    if url:
        response = requests.get(url)
        if response.status_code == 200:
            filtered_row = df[df['id'] == spotify_id]
            if not filtered_row.empty:
                artist_names = filtered_row['artists'].values[0]
                song_name = filtered_row['name'].values[0]

                file_name = clean_file_name(artist_names) + '_' + clean_file_name(song_name)
                file_name += '.mp3'  # Add file extension
            folder_name = './audio/input/random_songs'
            os.makedirs(folder_name, exist_ok=True)
            
            with open(os.path.join(folder_name, file_name), 'wb') as f:
                f.write(response.content)
        else:
            print(f"{spotify_id} preview is not available")
            return spotify_id
    else:
        print(f"spotify api cannot find preview url for {spotify_id}")
        return spotify_id
    
def move_files():
    # Distribute 10 files to each subfolder
    seed_song_list = os.listdir('./audio/seed_songs')
    all_files = [file for file in os.listdir('./audio/input/random_songs') if os.path.isfile(os.path.join('./audio/input/random_songs', file)) and file.endswith('.mp3')]
    for seed_song in seed_song_list: 
        seed_song = seed_song[:-4]
        for j in range(10):
            file_to_move = all_files.pop()  # Remove and get the last file from the list
            src = os.path.join(f'./audio/input/random_songs', file_to_move)
            
            dst = os.path.join(f'./audio/input/random_songs/{seed_song}', file_to_move)
            os.makedirs(dst, exist_ok=True)
            shutil.move(src, dst)

def random_main():
    create_directories()
    df = add_user_songs_if_not_exists()
    count = 0
    while count < 50:
        random_id = df['id'].sample(n=1, random_state=np.random.RandomState(42)).values[0]
        _, url = get_preview_url(random_id)
        result = get_preview_random_audio(df, random_id, url)
        if not result:
            count += 1
        print(len(os.listdir('random_songs')))
    move_files()
    



if __name__ == "__main__":
    similarity_based_main()
    random_main()