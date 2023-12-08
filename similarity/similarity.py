import tensorflow.compat.v1 as tf
import numpy as np
import soundfile as sf
import vggish_embeddings
from sklearn.metrics.pairwise import cosine_similarity

# def read_embeddings_from_tfrecord(tfrecord_file):
#     """read embeddings from tfrecord

#     Args:
#         tfrecord_file: 

#     Returns:
#         (num_frames, 128) -> 128 is from VGGish
#     """
#     # Define the feature name you used when writing the TFRecord.
#     feature_name = 'audio_embedding'
#     record_iterator = tf.python_io.tf_record_iterator(path=tfrecord_file)
#     embedding_matrix = []
#     print(record_iterator)
#     for string_record in record_iterator:
#         #string_record = next(record_iterator)
#         # Create a list to store the embeddings.
#         print(f"EMBEDDING: {string_record}")
#         example = tf.train.SequenceExample()
#         example.ParseFromString(string_record)
#         hexembed = example.feature_lists.feature_list['audio_embedding'].feature[0].bytes_list.value[0].hex()
#         arrayembed = [int(hexembed[i:i+2],16) for i in range(0,len(hexembed),2)]
#         # print(arrayembed)
#         embedding_matrix += [arrayembed]
#     embedding_matrix = np.array(embedding_matrix)
#     print(f"Embedding matrix: {embedding_matrix} \n Shape: {embedding_matrix.shape}")
#     return embedding_matrix



def feature_alignment_repeat(embedding1, embedding2):
    num_row_embed1 = embedding1.shape[0]
    num_row_embed2 = embedding2.shape[0]
    num_col_embed1 = embedding1.shape[1]
    num_col_embed2 = embedding2.shape[1]
    if num_row_embed1 > num_row_embed2:
        # embedding2 = np.vstack(embedding2, embedding2[:(len_embed1-len_embed2), :])
        embedding2 = np.tile(embedding2, (num_row_embed1 // num_row_embed2, 1))
        remaining_rows = num_row_embed1 % num_row_embed2
        if remaining_rows > 0:
            embedding2 = np.vstack((embedding2, embedding2[:remaining_rows, :]))

    if num_row_embed1 < num_row_embed2:
        # embedding1 = np.vstack(embedding1, embedding1[:(len_embed2-len_embed1), :])
        embedding1 = np.tile(embedding1, (num_row_embed2 // num_row_embed1, 1))
        remaining_rows = num_row_embed2 % num_row_embed1
        if remaining_rows > 0:
            embedding1 = np.vstack((embedding1, embedding1[:remaining_rows, :]))

    if num_col_embed1 > num_col_embed2:
        # embedding2 = np.vstack(embedding2, embedding2[:(len_embed1-len_embed2), :])
        embedding2 = np.tile(embedding2, (1, num_col_embed1 // num_col_embed2))
        remaining_cols = num_col_embed1 % num_col_embed2
        if remaining_cols > 0:
            embedding2 = np.hstack((embedding2, embedding2[:, :remaining_cols]))
    if num_col_embed1 < num_col_embed2:
        # embedding2 = np.vstack(embedding2, embedding2[:(len_embed1-len_embed2), :])
        embedding1 = np.tile(embedding1, (1, num_col_embed2 // num_col_embed1))
        remaining_cols = num_col_embed2 % num_col_embed1
        if remaining_cols > 0:
            embedding1 = np.hstack((embedding1, embedding1[:, :remaining_cols]))
    assert len(embedding1) == len(embedding2), f"Your embedding1 shape is {len(embedding1)}. Your embedding2 shape is {len(embedding2)}"
    assert embedding1.shape[1] == embedding2.shape[1],  f"Your embedding1 num_col is {num_col_embed1}. Your embedding2 num_col is {num_col_embed2}"
    return embedding1, embedding2

def feature_alignment_clip(embedding1, embedding2):
    
    num_row_embed1 = embedding1.shape[0]
    num_row_embed2 = embedding2.shape[0]
    num_col_embed1 = embedding1.shape[1]
    num_col_embed2 = embedding2.shape[1]
    if num_row_embed1 >  num_row_embed2:
        embedding1 = embedding1[:num_row_embed2, :]
        
    if num_row_embed1 < num_row_embed2:
        embedding2 = embedding2[:num_row_embed1, :]
    
    if num_col_embed1 > num_col_embed2:
        embedding1 = embedding1[:, :num_col_embed2]
    
    if num_col_embed1 < num_col_embed2:
        embedding2 = embedding2[:, :num_col_embed1]
    assert len(embedding1) == len(embedding2), f"Your embedding1 num_row is {len(embedding1)}. Your embedding2 num_row is {len(embedding2)}"
    assert embedding1.shape[1] == embedding2.shape[1],  f"Your embedding1 num_col is {num_col_embed1}. Your embedding2 num_col is {num_col_embed2}"
    return embedding1, embedding2
        

def cosine_sim(embedding1, embedding2, feature_alignment):
    # Calculate cosine similarity between two embeddings.
    # embedding1 = read_embeddings_from_tfrecord(tfrecord1)
    # embedding2 = read_embeddings_from_tfrecord(tfrecord2)
    if feature_alignment == "repeat":
        embedding1_align, embedding2_align = feature_alignment_repeat(embedding1, embedding2)
    if feature_alignment == "clip":
        embedding1_align, embedding2_align = feature_alignment_clip(embedding1, embedding2)
    # dot_product = np.dot(embedding1, embedding2.T)
    # norm1 = np.linalg.norm(embedding1)
    # norm2 = np.linalg.norm(embedding2)
    # similarity = dot_product / (norm1 * norm2)
    # Flatten the matrices
    #print(f"embedding1 aligned shape: {embedding1_align.shape} \n embedding2 aligned shape: {embedding2_align.shape}")
    flat_matrix1 = embedding1_align.flatten()
    flat_matrix2 = embedding2_align.flatten()

    # Reshape the flattened arrays to be 2D
    flat_matrix1 = flat_matrix1.reshape(1, -1)
    flat_matrix2 = flat_matrix2.reshape(1, -1)

    # Calculate cosine similarity
    similarity_score = cosine_similarity(flat_matrix1, flat_matrix2)[0, 0]

    return similarity_score



# if __name__ == '__main__':
# #     raw_dataset = tf.data.TFRecordDataset("./vggish-embeddings/01-D_AMairena.tfrecord")
# #     for raw_record in raw_dataset.take(1):
# #         example = tf.train.Example()
# #         example.ParseFromString(raw_record.numpy())
# #         print(f"Hello?{example}")
#     read_embeddings_from_tfrecord("./vggish-embeddings/ver 1.tfrecord")
    # Specify the path to your TFRecord files.
    # tfrecord_file = ['./vggish-embeddings/01-D_AMairena.tfrecord', './vggish-embeddings/63-M2_AMairena.tfrecord']


#     # Read the embeddings from the TFRecord files.
#     embeddings1 = read_embeddings_from_tfrecord(tfrecord_file[0])
#     embeddings2 = read_embeddings_from_tfrecord(tfrecord_file[1])

#     # Calculate cosine similarity between the embeddings (assuming you have two embeddings).
#     # You should loop through the embeddings to compare them individually.
#     print(f"Embedding1: \n {embeddings1} \n EMBEDDING 2: \n{embeddings2}")

#     similarity = cosine_similarity(embeddings1, embeddings2)


#     # Print the cosine similarities.
#     print(f'Cosine Similarities: {similarity}')

