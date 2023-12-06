import librosa
import numpy as np
import os
import pandas as pd
import similarity
import config
import baseline_main as bm
import vggish_main as vm
import vggish_embeddings

SEED_SONG = config.SEED_SONG
FEATURE_ALIGNMENT = config.FEATURE_ALIGNMENT
BLOCK_SIZE = config.BLOCK_SIZE
SAMPLING_RATE = config.SAMPLING_RATE

def get_features(audio_file, only_mfccs=False):
    VGGISH_WINDOW = 0.25
    BLOCK_SIZE = int(VGGISH_WINDOW*SAMPLING_RATE)
    audio_features = bm.get_audio_features(audio_file=audio_file, block_size=BLOCK_SIZE, hop_size=BLOCK_SIZE)
    vgg = vggish_embeddings.CreateVGGishNetwork(VGGISH_WINDOW)
    x, sr = librosa.load(audio_file, sr=SAMPLING_RATE, mono=True)
    vgg_embedding, _ = vm.extract_vggish(vgg, x, sr, postprocess=False)
    print(f"Length of your audio: {len(x)}, time = {len(x) / SAMPLING_RATE}" )
    assert audio_features.shape[1] == vgg_embedding.T.shape[1], f"Your audio features shape: {audio_features.shape}, your vggish embeddings shape: {vgg_embedding.shape}"
    
    return vgg_embedding

if __name__ == "__main__":
    get_features("./trainData/" + SEED_SONG)
    
    