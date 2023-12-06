import numpy as np
import pandas as pd
import librosa
import vggish_main
import similarity
import baseline_main
import baseline_vggish
import config
import os
import tqdm
import vggish_embeddings


folder_path = config.FOLDER_PATH
all_methods = config.ALL_METHODS
vggish_window = config.VGGISH_WINDOW

def similarity(folder_path=folder_path, method:list=all_methods) -> dict:

    dict_value_matrix = []
    audios = [f for f in os.listdir(folder_path) if f.endswith(".wav")]
    vgg = vggish_embeddings.CreateVGGishNetwork(vggish_window)
    for m in method:
        # for f in audios:
        print(m)
        # audio_path = os.path.join(folder_path, f)

        if m == "vggish":
            dict_value_matrix += [vggish_main.vggish_similarity_rank(audio_path=folder_path, vgg=vgg)]
            continue
        if m =="baseline_all":
            dict_value_matrix += [baseline_main.baseline_similarity_rank(audio_path=folder_path, only_mfccs=False)]
            continue
        if m == "baseline_mfccs":
            dict_value_matrix += [baseline_main.baseline_similarity_rank(audio_path=folder_path, only_mfccs=True)]
            continue
        if m == "combined_all":
            dict_value_matrix += [baseline_vggish.combine_feature_similarity_rank(audio_path=folder_path, vgg=vgg, only_mfccs=False)]
            continue
        if m == "combined_mfccs":
            dict_value_matrix += [baseline_vggish.combine_feature_similarity_rank(audio_path=folder_path, vgg=vgg, only_mfccs=True)]
            continue
        else:
            raise ValueError(f"Your method name: {m} is not right. Please check comments in config.py")
            
    
    
    similarity_dict = dict(zip(method, dict_value_matrix))
    
    print(f"Similarity dictionary: {similarity_dict} \n Similarity keys: {similarity_dict.keys()} \n Similarity values: {similarity_dict.values()}")
    
    
    
    return similarity_dict

if __name__ == "__main__":
    similarity()

