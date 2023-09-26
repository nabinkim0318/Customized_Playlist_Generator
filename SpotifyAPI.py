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

ranges = ['short_term', 'medium_term', 'long_term']

for sp_range in ranges:
    print("range:", sp_range)
    results = sp.current_user_top_tracks(time_range=sp_range, limit=50)
    for i, item in enumerate(results['items']):
        print(i, item['name'], '//', item['artists'][0]['name'])
    print()
