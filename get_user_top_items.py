import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import os

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="0c8dbb1cfb78479d9613930fbc9ad872",
    client_secret="260a210533424c4592cb3d24d1da7b85",
    redirect_uri="https://www.audiocontentanalysis.org",
    scope="user-top-read",
))

# debugging stuffs 
# create a new folder called similarity_based (put five seed songs)
# create a new folder called random (put five seed songs)

def get_audio_features(track_id):
    audio_features = sp.audio_features(track_id)
    if audio_features:
        return audio_features[0]
    else:
        return None


def preprocess_track_features(track_info, audio_features):
    track_id = track_info['id']
    track_name = track_info['name']
    album_info = track_info['album']
    album_name = album_info['name']
    album_id = album_info['id']
    artists_info = track_info['artists']
    artists_names = [artist['name'] for artist in artists_info]
    artist_ids = [artist['id'] for artist in artists_info]
    track_number = track_info['track_number']
    disc_number = track_info['disc_number']
    explicit = track_info['explicit']

    if audio_features:
        danceability = audio_features['danceability']
        energy = audio_features['energy']
        key = audio_features['key']
        loudness = audio_features['loudness']
        mode = audio_features['mode']
        speechiness = audio_features['speechiness']
        acousticness = audio_features['acousticness']
        instrumentalness = audio_features['instrumentalness']
        liveness = audio_features['liveness']
        valence = audio_features['valence']
        tempo = audio_features['tempo']
        duration_ms = audio_features['duration_ms']
        time_signature = audio_features['time_signature']
    else:
        danceability = energy = key = loudness = mode = speechiness = acousticness = \
            instrumentalness = liveness = valence = tempo = duration_ms = time_signature = None

    release_date = album_info['release_date'].split('-')[0]

    each_track_info = {
        "id": track_id,
        "name": track_name,
        "album": album_name,
        "album_id": album_id,
        "artists": ', '.join(artists_names),
        "artist_ids": ', '.join(artist_ids),
        "track_number": track_number,
        "disc_number": disc_number,
        "explicit": explicit,
        "danceability": danceability,
        "energy": energy,
        "key": key,
        "loudness": loudness,
        "mode": mode,
        "speechiness": speechiness,
        "acousticness": acousticness,
        "instrumentalness": instrumentalness,
        "liveness": liveness,
        "valence": valence,
        "tempo": tempo,
        "duration_ms": duration_ms,
        "time_signature": time_signature,
        "year": release_date,
        "release_date": album_info['release_date']
    }
    return each_track_info

def print_top_items():
    ranges = ['short_term', 'medium_term', 'long_term']

    for sp_range in ranges:
        print("range:", sp_range)
        results = sp.current_user_top_tracks(time_range=sp_range, limit=50)

        track_data = []
        for i, item in enumerate(results['items']):
            #print(i, item['name'], '//', item['artists'][0]['name'])

            track_id = item['id']
            audio_features = get_audio_features(track_id)
            each_track_info = preprocess_track_features(item, audio_features)
            track_data.append(each_track_info)

        df = pd.DataFrame(track_data)
        #print(df)
        if not os.path.exists("./user_top_items/"):
            os.mkdir("./user_top_items")

        df.to_csv(f'./user_top_items/top_tracks_{sp_range}.csv', index=False)
