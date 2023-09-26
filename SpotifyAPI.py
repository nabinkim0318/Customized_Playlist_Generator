import spotipy
from spotipy.oauth2 import SpotifyOAuth

# run -> type redirect uri -> get info

# Spotify API auth
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="0c8dbb1cfb78479d9613930fbc9ad872",
    client_secret="260a210533424c4592cb3d24d1da7b85",
    redirect_uri="https://www.audiocontentanalysis.org", # changed because Github uri might not be used 
    scope="user-top-read",
    username="luhee shin"
))

# short_term (4 weeks)
time_range = "short_term"  

# 10 top artists, tracks
top_artists = sp.current_user_top_artists(time_range=time_range, limit=10)
top_tracks = sp.current_user_top_tracks(time_range=time_range, limit=10)

print("Top artists:")
for idx, artist in enumerate(top_artists['items'], start=1):
    print(f"{idx}. {artist['name']}")

print("\nTop tracks:")
for idx, track in enumerate(top_tracks['items'], start=1):
    print(f"{idx}. {track['name']} - {', '.join([artist['name'] for artist in track['artists']])}")
