import requests
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans, DBSCAN
from sklearn.mixture import GaussianMixture
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score


def get_top_tracks_href(type="tracks", time_range="medium_term", limit=20, offset=0, access_token):
    # Define the base URL for the API endpoint
    base_url = "https://api.spotify.com/v1/me/top/tracks"

    # Set the API endpoint parameters
    params = {
        "time_range": time_range,
        "limit": limit,
        "offset": offset
    }

    # Replace 'ACCESS_TOKEN' with the Spotify access token
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    # Make the GET request
    response = requests.get(url, params=params, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        data = response.json()
        # Extract the 'href' value from the response
        href = data.get('href')
        return href  # Return the 'href' value
        
    else:
        # If the request was not successful, print an error message
        print(f"Error: {response.status_code}")
        return None
        

def get_full_json_response(href_url, limit=None):
    try:
        top_top_items_list = []
        while href_url:
            response = requests.get(href_url)
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx and 5xx)

            # Check if the response is JSON
            if 'application/json' in response.headers.get('content-type', ''):
                data = response.json()
                top_items_list.extend(data.get('items', []))  # Append the items to the top_items_list

                # If there's a 'next' URL, update 'href_url' to fetch the next page
                href_url = data.get('next')

                # If 'limit' is provided and we've fetched enough items, break the loop
                if limit is not None and len(top_items_list) >= limit:
                    break
            else:
                print("The response is not in JSON format.")
                return None

        return top_items_list
    except requests.exceptions.RequestException as e:
        print(f"Error making HTTP request: {e}")
        return None
    

def preprocess_track_features(top_items_list):
    # preprocess the spotify api's information to match with the MSD dataset
    track_data = []

    for top_item in top_items_list:
        each_track_info = {
            "spotify_url": top_item["external_urls"]["spotify"],
            "total_followers": top_item["followers"]["total"],
            "genres": ", ".join(top_item["genres"]),
            "href": top_item["href"],
            "artist_id": top_item["id"],
            "image_url": top_item["images"][0]["url"],
            "artist_name": top_item["name"],
            "popularity": top_item["popularity"],
            "artist_type": top_item["type"],
            "uri": top_item["uri"]
        }
        track_data.append(each_track_info)
        
    df = pd.DataFrame(track_data)
    return df


def preprocess_track_analysis(top_items_list):
    # concatenated features that are inside the audio analysis from spotify API
    print()


if __name__ == "__main__":
    href_url = get_top_tracks_href(type="tracks", time_range="medium_term", limit=20, offset=0)
    top_items_list = get_full_json_response(href_url, limit)
    
    if top_items_list is not None:
        print("Full JSON Response:")
        print(top_items_list)
    else:
        print("Failed to retrieve the JSON response.")
    
    df = preprocess_track_data(top_items_list)

    
