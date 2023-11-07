import yt_dlp
import requests
import os

import yt_dlp

def find_youtube_audio_url(track_info, api_key):
    try:
        query = f"{track_info} official audio"
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "key": api_key,
            "q": query,
            "maxResults": 1,  
            "type": "video"  
        }
        response = requests.get(url, params=params)

        # Check for a successful response
        if response.status_code == 200:
            data = response.json()
            if "items" in data:
                # Extract the audio URL from the first result
                if data["items"]:
                    video_id = data["items"][0]["id"]["videoId"]
                    youtube_url = f"https://www.youtube.com/watch?v={video_id}"
                    return youtube_url
                else:
                    return "No matching audio tracks found."
            else:
                return "No 'items' field in the response."
        else:
            return f"Error ({response.status_code}): {response.text}"
    except Exception as e:
        return f"An error occurred: {str(e)}"


def download_audio(url, output_directory, track_info):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_directory, f'{track_info}'),
        'verbose': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def download_audio_given_list(track_list, output_directory, api_key):
    for track_info in track_list[1:]:
        youtube_url = find_youtube_audio_url(track_info, api_key)

        if youtube_url:
            print(f"YouTube Audio URL for {track_info}: {youtube_url}")
            download_audio(youtube_url, output_directory, track_info)
        else:
            print(f"Could not find a YouTube audio URL for {track_info}")

    
if __name__ == "__main__":
    # Constants 
    DAY = 0              # replace with your actual day 
    TOTAL_SONG = 300     # replace with your number of songs 
    SONGS_PER_DAY = 100
    
    f = open("Nabin_0:400_sliced_data.txt", "r") # replace with your actual file name
    track_list = f.read() 
    track_list = data.split("\n") 
    track_list.pop(TOTAL_SONG) # pop abnormal ' ' at the end of the list 
    f.close() 
    
    api_key = " " # replace with your API key 
    home_directory = os.path.expanduser("~")
    output_directory = os.path.join(home_directory, "Downloads")
    download_audio_given_list(track_list[DAY*SONGS_PER_DAY:(DAY+1)*SONGS_PER_DAY], output_directory, api_key)
