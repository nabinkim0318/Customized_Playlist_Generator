# Customized Playlist Generator

### Usage instruction

Before you run our project, please install all required packages:
```python
python3 -m pip install -r requirements.txt
```

To use your own Spotify top 5 items, cd into the root folder and run ```python3 main.py```

You will be redirected to a [website](https://www.audiocontentanalysis.org/). Authorize your account and copy the website url as is in the address bar into the prompted input box in terminal.

In about 5 minutes, the output songs will be in the folder ```./audio/output/<low_level_feature_name>/<high_level_feature_type>/<seed_song_name>/<recommended song 1.mp3>```

We have used your GATECH email to add you as a developer for the above step to work. If you have a different email associated with your Spotify account, please reach out to us.


Note: since our project doesn't involve testing, inside the test folder, you will see an example input and output folder with example audio files. 

We recommend running this repo as is instead of unzipping the code in the src folder. 

### Folder Structure
```
├── src
│   ├── code_only.zip
├── eval
│   ├── predictions
│   │   ├── random/method/prediction.csv
│   │   ├── similarity/method/prediction.csv
│   ├── eval_main.py
│   ├── metrics.py
│   ├── prediction_rank.py
│   ├── similarity.py
├── ext/audioset
├── similarity # experiment code
│   ├── audioset
│   ├── baseline_main.py
│   ├── baseline_vggish.py
│   ├── vggish_main.py
....
├── test
│   ├── audio
│   │   ├── input/similarity_based/<seed song folder>/
│   │   ├── output/<method>/similarity_based/<seed song folder>/
│   │   ├── seed_songs/<seed_song.mp3>
├── config.py
├── **main.py**
...
└── .gitignore

```


