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


def download_audio(url, output_directory, track_info):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_directory, f'{track_info}.mp3'),
        'verbose': True
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def download_audio_given_list(track_list, output_directory, api_key):
    for track_info in track_list:
        youtube_url = find_youtube_audio_url(track_info, api_key)

        if youtube_url:
            print(f"YouTube Audio URL for {track_info}: {youtube_url}")
            download_audio(youtube_url, output_directory, track_info)
        else:
            print(f"Could not find a YouTube audio URL for {track_info}")

    
if __name__ == "__main__":
    # Testings are done
    songs = [ "STAY (with Justin Bieber) The Kid LAROI", "Star Colde", "Watermelon Sugar Harry Styles", 
             "Sure Thing Miguel", "Lil Bit Nelly", "Numb Marshmello", 
             "Dance The Night - From Barbie The Album Dua Lipa", "Unstoppable Sia", 
             "Someone To You BANNERS", "2 Be Loved (Am I Ready) Lizzo", "Fly Away Tones And I", 
             "Levitating (feat. DaBaby) Dua Lipa", "I Ain't Worried OneRepublic", "Victoria's Secret Jax",
             "Clarity Vance Joy", "Waffle House Jonas Brothers", "Big Energy Latto", 
             "If We Ever Broke Up Mae Stephens", "Cold Heart - PNAU Remix Elton John" ]
    api_key = "API_KEY"    
    home_directory = os.path.expanduser("~")
    output_directory = os.path.join(home_directory, "Downloads")
    download_audio_given_list(track_list, output_directory, api_key)
