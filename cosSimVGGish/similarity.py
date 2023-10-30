import tensorflow.compat.v1 as tf
import numpy as np

def read_embeddings_from_tfrecord(tfrecord_file):
    # Define the feature name you used when writing the TFRecord.
    feature_name = 'audio_embedding'
    record_iterator = tf.python_io.tf_record_iterator(path=tfrecord_file)
    string_record = next(record_iterator)
    # Create a list to store the embeddings.
    embeddings = []
    example = tf.train.SequenceExample()
    example.ParseFromString(string_record)
    hexembed = example.feature_lists.feature_list['audio_embedding'].feature[0].bytes_list.value[0].hex()
    arrayembed = [int(hexembed[i:i+2],16) for i in range(0,len(hexembed),2)]
    print(arrayembed)

    return np.array(arrayembed)

def cosine_similarity(embedding1, embedding2):
    # Calculate cosine similarity between two embeddings.
    # embedding1 = read_embeddings_from_tfrecord(tfrecord1)
    # embedding2 = read_embeddings_from_tfrecord(tfrecord2)
    
    dot_product = np.dot(embedding1, embedding2)
    norm1 = np.linalg.norm(embedding1)
    norm2 = np.linalg.norm(embedding2)
    similarity = dot_product / (norm1 * norm2)
    return similarity

# if __name__ == '__main__':
#     # Specify the path to your TFRecord files.
#     tfrecord_file = ['./vggish-embeddings/01-D_AMairena.tfrecord', './vggish-embeddings/63-M2_AMairena.tfrecord']


#     # Read the embeddings from the TFRecord files.
#     embeddings1 = read_embeddings_from_tfrecord(tfrecord_file[0])
#     embeddings2 = read_embeddings_from_tfrecord(tfrecord_file[1])

#     # Calculate cosine similarity between the embeddings (assuming you have two embeddings).
#     # You should loop through the embeddings to compare them individually.
#     print(f"Embedding1: \n {embeddings1} \n EMBEDDING 2: \n{embeddings2}")

#     similarity = cosine_similarity(embeddings1, embeddings2)


#     # Print the cosine similarities.
#     print(f'Cosine Similarities: {similarity}')

