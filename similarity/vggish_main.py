import vggish_embeddings
import similarity
import os
import pandas as pd
import tensorflow.compat.v1 as tf
import librosa
import config

SEED_SONG = config.SEED_SONG
FEATURE_ALIGNMENT = config.FEATURE_ALIGNMENT
SAMPLING_RATE = config.SAMPLING_RATE


def extract_vggish(vgg, x, sr, postprocess=False):
    if postprocess: 
        embedding = vggish_embeddings.ProcessWithVGGish(vgg, x, sr)
        str_process = "postprocess"

    else:
        embedding = vggish_embeddings.EmbeddingsFromVGGish(vgg, x, sr)["embedding"]
        str_process = "preprocess"
        
    
    return embedding, str_process


def vggish_similarity_rank(audio_path, vgg):

    audios = [f for f in os.listdir(audio_path) if f.endswith(".wav")]
    file_embed_dict = {}
    # vgg = vggish_embeddings.CreateVGGishNetwork(0.96)
    for f in audios:
        print(f)
        x, sr = librosa.load(audio_path + f, sr = SAMPLING_RATE, mono=True)
        #resdict = vggish_embeddings.EmbeddingsFromVGGish(vgg, x, sr)
        #file_embed_dict[f] = resdict["embedding"]
        embedding, str_process = extract_vggish(vgg, x, sr, postprocess=False)
        file_embed_dict[f] = embedding
    
    trainData_embedding_df = pd.DataFrame({"name": file_embed_dict.keys(), "embedding": file_embed_dict.values()})
    similarities = []

    song_index = trainData_embedding_df[trainData_embedding_df["name"] == SEED_SONG].index.tolist()
    seed_embedding = trainData_embedding_df.loc[song_index[0], "embedding"]
    for i in range(len(trainData_embedding_df)):
        current_embedding = trainData_embedding_df.loc[i, "embedding"]
        assert seed_embedding.dtype == current_embedding.dtype, f"SEED dtype:{seed_embedding.dtype} CURRENT dypte: {current_embedding.dtype} "
        sim = similarity.cosine_sim(seed_embedding, current_embedding, FEATURE_ALIGNMENT)
        similarities += [sim]
        print(sim)
    
    trainData_embedding_df["similarities"] = similarities
    print(trainData_embedding_df)
    #trainData_embedding_df.to_csv(f"./similarity_results/{str_process}_{feature_alignment}_{SEED_SONG}_similarities.csv", index=False)
    return trainData_embedding_df.sort_values(by="similarities", ascending=False)
    



def main(_):
    vggish_similarity_rank("./trainData/")
    
    
    
    

    


if __name__ == "__main__":
    tf.app.run()
