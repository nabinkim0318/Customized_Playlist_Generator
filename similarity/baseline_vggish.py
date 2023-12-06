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
VGGISH_WINDOW = config.VGGISH_WINDOW
def get_combined_features(audio_file, vggmodel, only_mfccs=False, postprocess=False):

    BLOCK_SIZE = int(VGGISH_WINDOW*SAMPLING_RATE)
    if only_mfccs:
        audio_features = bm.get_only_mfccs(audio_file=audio_file, block_size=BLOCK_SIZE, hop_size=BLOCK_SIZE)
    else:
        audio_features = bm.get_audio_features(audio_file=audio_file, block_size=BLOCK_SIZE, hop_size=BLOCK_SIZE)

    x, sr = librosa.load(audio_file, sr=SAMPLING_RATE, mono=True)
    vgg_embedding, _ = vm.extract_vggish(vggmodel, x, sr, postprocess=postprocess)
    vgg_embedding = vgg_embedding.T
    print(f"Length of your audio: {len(x)}, time = {len(x) / SAMPLING_RATE}" )
    min_len = min(vgg_embedding.shape[1], audio_features.shape[1])
    vgg_embedding = vgg_embedding[:, :min_len]
    audio_features = audio_features[:, :min_len]
    assert audio_features.shape[1] == vgg_embedding.shape[1], f"Your audio features shape: {audio_features.shape}, your vggish embeddings shape: {vgg_embedding.shape}"
    comb_features = np.vstack([audio_features, vgg_embedding])
    print(comb_features.shape)
    return comb_features

def combine_feature_similarity_rank(audio_path, vgg, only_mfccs=False):
    audios = [f for f in os.listdir(audio_path) if f.endswith(".wav")]
    file_feature_dict = {}
    # vgg = vggish_embeddings.CreateVGGishNetwork(VGGISH_WINDOW)
    for f in audios:
        print(f)
        comb_features = get_combined_features(audio_file=audio_path + f, only_mfccs=only_mfccs, vggmodel=vgg)
        
        file_feature_dict[f] = comb_features
    
    trainData_feature_df = pd.DataFrame({"name": file_feature_dict.keys(), "feature": file_feature_dict.values()})
    similarities = []
    
    song_index = trainData_feature_df[trainData_feature_df["name"] == SEED_SONG].index.tolist()
    seed_feature = trainData_feature_df.loc[song_index[0], "feature"]
    for i in range(len(trainData_feature_df)):
        current_feature = trainData_feature_df.loc[i, "feature"]
        assert seed_feature.dtype == current_feature.dtype, f"SEED dtype:{seed_feature.dtype} CURRENT dypte: {current_feature.dtype} "
        name = trainData_feature_df.loc[i, "name"]
        print(f"Name of file with similarity issue: {name}")
        sim = similarity.cosine_sim(seed_feature, current_feature, FEATURE_ALIGNMENT)
        similarities += [sim]

    
    trainData_feature_df["similarities"] = similarities
    print(trainData_feature_df)
    #trainData_embedding_df.to_csv(f"./similarity_results/{str_process}_{feature_alignment}_{SEED_SONG}_similarities.csv", index=False)
    return trainData_feature_df.sort_values(by="similarities", ascending=False)
    

if __name__ == "__main__":
    combine_feature_similarity_rank(audio_path="./trainData/", only_mfccs=True).to_csv("only_mfccs_combined_features.csv")
    
    