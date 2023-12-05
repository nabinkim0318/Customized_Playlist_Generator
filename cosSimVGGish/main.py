import numpy as np
import pandas as pd
import librosa
import vggish_main
import soundfile as sf
import similarity

def similarity(folder_path, method):
    similarity_matrix = []    
    if method == "vggish":
        similarity_rank = vggish_main.vggish_similarity_rank(audio_path=folder_path)
    
    return similarity_matrix


    