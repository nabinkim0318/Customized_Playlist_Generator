import spotipy
from spotipy.oauth2 import SpotifyOAuth

# client info -> type redirect url -> get user's top tracks

# Spotify API auth
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
client_id="id here",
client_secret="secret here",
redirect_uri="uri here",
scope="user-top-read",
))

def get_audio_features(track_id):
audio_features = sp.audio_features(track_id)
    if audio_features:
        return audio_features[0]
    else:
        return None

ranges = ['short_term', 'medium_term', 'long_term']

for sp_range in ranges:
    print("range:", sp_range)
results = sp.current_user_top_tracks(time_range=sp_range, limit=50)
    for i, item in enumerate(results['items']):
        print(i, item['name'], '//', item['artists'][0]['name'])
        # track's audio features
track_id = item['id']
audio_features = get_audio_features(track_id)
            
        if audio_features:
            print("Audio Features:")
            print("Danceability:", audio_features['danceability'])
            print("Energy:", audio_features['energy'])
            print("Instrumentalness:", audio_features['instrumentalness'])
            print("Liveness:", audio_features['liveness'])    
    
    print()
