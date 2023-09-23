import requests

def get_top_tracks_or_artists(type="tracks", time_range="medium_term", limit=20, offset=0):
    # Define the base URL for the API endpoint
    base_url = "https://api.spotify.com/v1/me/top/{type}"

    # Set the API endpoint URL and parameters
    url = base_url.format(type=type)
    params = {
        "time_range": time_range,
        "limit": limit,
        "offset": offset
    }

    # Replace 'YOUR_ACCESS_TOKEN' with your Spotify access token
    headers = {
        "Authorization": "Bearer YOUR_ACCESS_TOKEN"
    }

    # Make the GET request
    response = requests.get(url, params=params, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the response JSON
        data = response.json()
        return data
    else:
        # If the request was not successful, print an error message
        print(f"Error: {response.status_code}")
        return None

# Example usage:
top_tracks = get_top_tracks_or_artists(type="tracks", time_range="medium_term", limit=20, offset=0)
