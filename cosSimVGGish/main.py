import vggish_embeddings
import similarity
import os
import pandas as pd
import tensorflow.compat.v1 as tf



def main(_):
    audio_path = "./trainData/"
    audios = [f for f in os.listdir(audio_path) if f.endswith(".wav")]
    file_embed_dict = {}
    
    for f in audios:
        print(f)
        embed = vggish_embeddings.read_vggish_embeddings(audio_path + f)
        file_embed_dict[f] = embed
        
    # tfrecord_path = "./vggish-embeddings/"
    # tfrecords = [f for f in os.listdir(tfrecord_path) if f.endswith(".tfrecord")]
    # name, embeddings, similarities = [], [], []
    # for f in tfrecords:
    #     name += [f.replace(".tfrecord", "")]
    #     embeddings += [similarity.read_embeddings_from_tfrecord(tfrecord_path + f)]
    #     print(f"length of embedding: {len(similarity.read_embeddings_from_tfrecord(tfrecord_path + f))} \n")
    
    
    trainData_embedding_df = pd.DataFrame({"name": file_embed_dict.keys(), "embedding": file_embed_dict.values()})
    similarities = []
    for i in range(len(trainData_embedding_df)):
        # using the first song as seed song
        seed_embedding = trainData_embedding_df.loc[3, "embedding"]
        current_embedding = trainData_embedding_df.loc[i, "embedding"]
        sim = similarity.cosine_sim(seed_embedding, current_embedding)
        similarities += [sim]
        print(sim)
    
    trainData_embedding_df["similarities"] = similarities
    print(trainData_embedding_df)
        
    
    
    
    

    


if __name__ == "__main__":
    tf.app.run()
