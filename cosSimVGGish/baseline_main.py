import librosa
import numpy as np
import os
import pandas as pd
import similarity
import config

SEED_SONG = config.SEED_SONG
FEATURE_ALIGNMENT = config.FEATURE_ALIGNMENT
BLOCK_SIZE = config.BLOCK_SIZE

def get_audio_features(audio_file, block_size = BLOCK_SIZE, hop_size = None):
    y, sr = librosa.load(audio_file, sr=None, mono=True)

    # Set default hop_size if not specified
    if hop_size is None:
        hop_size = block_size // 2

    rms = librosa.feature.rms(y=y, frame_length=block_size, hop_length=hop_size)[0]

    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr, n_fft=block_size, hop_length=hop_size)[0]

    spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr, n_fft=block_size, hop_length=hop_size)[0]

    spectral_flux = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop_size)

    spectral_crest = np.max(librosa.feature.spectral_centroid(y=y, sr=sr, n_fft=block_size, hop_length=hop_size), axis=1) / np.sum(librosa.feature.spectral_centroid(y=y, sr=sr, n_fft=block_size, hop_length=hop_size), axis=1)

    zero_crossings_rate = librosa.feature.zero_crossing_rate(y, frame_length=block_size, hop_length=hop_size)[0]

    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13, n_fft=block_size, hop_length=hop_size)

    min_len = min(len(rms), len(spectral_centroid), len(spectral_rolloff), len(spectral_flux), len(zero_crossings_rate), len(mfccs[0]))

    spectral_crest = np.full_like(rms, spectral_crest)

    feature_matrix = np.vstack([rms, spectral_centroid, spectral_rolloff, spectral_flux, spectral_crest, zero_crossings_rate, mfccs])

    return feature_matrix

def baseline_similarity_rank(audio_path):
    audios = [f for f in os.listdir(audio_path) if f.endswith(".wav")]
    file_feature_dict = {}
    for f in audios:
        print(f)
        feature = get_audio_features(audio_file=audio_path + f)
        file_feature_dict[f] = feature
    
    trainData_feature_df = pd.DataFrame({"name": file_feature_dict.keys(), "feature": file_feature_dict.values()})
    similarities = []
    
    song_index = trainData_feature_df[trainData_feature_df["name"] == SEED_SONG].index.tolist()
    seed_embedding = trainData_feature_df.loc[song_index[0], "feature"]
    for i in range(len(trainData_feature_df)):
        current_embedding = trainData_feature_df.loc[i, "feature"]
        assert seed_embedding.dtype == current_embedding.dtype, f"SEED dtype:{seed_embedding.dtype} CURRENT dypte: {current_embedding.dtype} "
        sim = similarity.cosine_sim(seed_embedding, current_embedding, FEATURE_ALIGNMENT)
        similarities += [sim]
        print(sim)
    
    trainData_feature_df["similarities"] = similarities
    print(trainData_feature_df)
    #trainData_embedding_df.to_csv(f"./similarity_results/{str_process}_{feature_alignment}_{SEED_SONG}_similarities.csv", index=False)
    return trainData_feature_df.sort_values(by="similarities", ascending=False)


if __name__ == "__main__":
    baseline_similarity_rank("./trainData/")