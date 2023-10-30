import extract_vggish
import os
import pandas as pd
import tensorflow.compat.v1 as tf
import similarity


def main(_):
    audio_path = "./trainData/"
    audios = [f for f in os.listdir(audio_path) if f.endswith(".wav")]
    for f in audios:
        print(f)
        extract_vggish.write_vggish_per_file(audio_path+f)
    tfrecord_path = "./vggish-embeddings/"
    tfrecords = [f for f in os.listdir(tfrecord_path) if f.endswith(".tfrecord")]
    name, embeddings, similarities = [], [], []
    for f in tfrecords:
        name += [f.replace(".tfrecord", "")]
        embeddings += [similarity.read_embeddings_from_tfrecord(tfrecord_path + f)]
        print(f"length of embedding: {len(similarity.read_embeddings_from_tfrecord(tfrecord_path + f))} \n")
    
    trainData_embedding_df = pd.DataFrame({"name": name, "embedding": embeddings})

    for i in range(len(trainData_embedding_df)):
        # using the first song as seed song
        seed_embedding = trainData_embedding_df.loc[9, "embedding"]
        current_embedding = trainData_embedding_df.loc[i, "embedding"]
        similarities += [similarity.cosine_similarity(seed_embedding, current_embedding)]
    
    trainData_embedding_df["similarities"] = similarities
    print(trainData_embedding_df)
        
    
    
    
    

    


if __name__ == "__main__":
    tf.app.run()
