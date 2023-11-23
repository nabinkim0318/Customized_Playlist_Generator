import vggish_embeddings
import similarity
import os
import pandas as pd
import tensorflow.compat.v1 as tf
import soundfile as sf



def extract_vggish(vgg, x, sr, postprocess=False, feature_alignment="repeat"):
    if postprocess: 
        embedding = vggish_embeddings.ProcessWithVGGish(vgg, x, sr)
        str_process = "postprocess"

    else:
        embedding = vggish_embeddings.EmbeddingsFromVGGish(vgg, x, sr)["embedding"]
        str_process = "preprocess"
        
    
    return embedding, str_process, feature_alignment
    



def main(_):
    audio_path = "./trainData/"
    audios = [f for f in os.listdir(audio_path) if f.endswith(".wav")]
    file_embed_dict = {}
    vgg = vggish_embeddings.CreateVGGishNetwork(0.96)
    for f in audios:
        print(f)
        x, sr = sf.read(audio_path + f)
        #resdict = vggish_embeddings.EmbeddingsFromVGGish(vgg, x, sr)
        #file_embed_dict[f] = resdict["embedding"]
        embedding, str_process, feature_alignment = extract_vggish(vgg, x, sr, postprocess=False, feature_alignment="clip")
        file_embed_dict[f] = embedding
        
    # tfrecord_path = "./vggish-embeddings/"
    # tfrecords = [f for f in os.listdir(tfrecord_path) if f.endswith(".tfrecord")]
    # name, embeddings, similarities = [], [], []
    # for f in tfrecords:
    #     name += [f.replace(".tfrecord", "")]
    #     embeddings += [similarity.read_embeddings_from_tfrecord(tfrecord_path + f)]
    #     print(f"length of embedding: {len(similarity.read_embeddings_from_tfrecord(tfrecord_path + f))} \n")
    
    
    trainData_embedding_df = pd.DataFrame({"name": file_embed_dict.keys(), "embedding": file_embed_dict.values()})
    similarities = []
    SEED_SONG = "01-D_AMairena.wav"
    song_index = trainData_embedding_df[trainData_embedding_df["name"] == SEED_SONG].index.tolist()
    seed_embedding = trainData_embedding_df.loc[song_index[0], "embedding"]
    for i in range(len(trainData_embedding_df)):
        # using the first song as seed song
        
        current_embedding = trainData_embedding_df.loc[i, "embedding"]
        assert seed_embedding.dtype == current_embedding.dtype, f"SEED dtype:{seed_embedding.dtype} CURRENT dypte: {current_embedding.dtype} "
        sim = similarity.cosine_sim(seed_embedding, current_embedding, feature_alignment)
        similarities += [sim]
        print(sim)
    
    trainData_embedding_df["similarities"] = similarities
    print(trainData_embedding_df)
    trainData_embedding_df.to_csv(f"./similarity_results/{str_process}_{feature_alignment}_{SEED_SONG}_similarities.csv", index=False)
        
    
    
    
    

    


if __name__ == "__main__":
    tf.app.run()
