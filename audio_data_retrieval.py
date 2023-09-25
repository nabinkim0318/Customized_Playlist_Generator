import youtube_dl
import requests

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


def download_audio(url, output_directory):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': f'{output_directory}/%(title)s.%(ext)s',
        'verbose': True
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


if __name__ == "__main__":
    # Testings are done
    api_key = "API_KEY"
    track_info = "Artist Song_Title"
    youtube_url = find_youtube_audio_url(artist, song_title, api_key)
    print(f"YouTube Audio URL: {youtube_url}")

    youtube_url = "https://www.youtube.com/watch?v=o2zHd4147sk"
    home_directory = os.path.expanduser("~")
    output_directory = os.path.join(home_directory, "Downloads")
    download_audio(youtube_url, output_directory)
