
from __future__ import print_function
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, './audioset/vggish'))

import numpy as np
import six
import soundfile
import tensorflow.compat.v1 as tf

import vggish_input
import vggish_params
import vggish_postprocess
import vggish_slim

flags = tf.app.flags

flags.DEFINE_string(
    'wav_file', '',
    'Path to a wav file. Should contain signed 16-bit PCM samples. '
    'If none is provided, a synthetic sound is used.')

flags.DEFINE_string(
    'checkpoint', './audioset/vggish/vggish_model.ckpt',
    'Path to the VGGish checkpoint file.')

flags.DEFINE_string(
    'pca_params', './audioset/vggish/vggish_pca_params.npz',
    'Path to the VGGish PCA parameters file.')
    
flags.DEFINE_string(
    'tfrecord_file','',
    'Path to a TFRecord file where embeddings will be written.')
    
FLAGS = flags.FLAGS

def write_vggish_per_file(wav_file_path):
  # In this simple example, we run the examples from a single audio file through
  # the model. If none is provided, we generate a synthetic input.
    FLAGS.wav_file = "./" + wav_file_path
    tfrecord_file_path = './vggish-embeddings/' + wav_file_path.split('/')[-1]
    tfrecord_file_path = tfrecord_file_path.replace(".wav", ".tfrecord")
    FLAGS.tfrecord_file = tfrecord_file_path


    
    print(f"ouput_file_path: {tfrecord_file_path}")
    examples_batch = vggish_input.wavfile_to_examples(FLAGS.wav_file)
    
    print(examples_batch)

    # Prepare a postprocessor to munge the model embeddings.
    pproc = vggish_postprocess.Postprocessor(FLAGS.pca_params)

    # If needed, prepare a record writer to store the postprocessed embeddings.
    writer = tf.python_io.TFRecordWriter(
        FLAGS.tfrecord_file) if FLAGS.tfrecord_file else None

    with tf.Graph().as_default(), tf.Session() as sess:
    # Define the model in inference mode, load the checkpoint, and
    # locate input and output tensors.
        vggish_slim.define_vggish_slim(training=False)
        vggish_slim.load_vggish_slim_checkpoint(sess, FLAGS.checkpoint)
        features_tensor = sess.graph.get_tensor_by_name(
            vggish_params.INPUT_TENSOR_NAME)
        embedding_tensor = sess.graph.get_tensor_by_name(
            vggish_params.OUTPUT_TENSOR_NAME)

        # Run inference and postprocessing.
        [embedding_batch] = sess.run([embedding_tensor],
                                        feed_dict={features_tensor: examples_batch})
        print(embedding_batch)
        postprocessed_batch = pproc.postprocess(embedding_batch)
        print(postprocessed_batch)

        # Write the postprocessed embeddings as a SequenceExample, in a similar
        # format as the features released in AudioSet. Each row of the batch of
        # embeddings corresponds to roughly a second of audio (96 10ms frames), and
        # the rows are written as a sequence of bytes-valued features, where each
        # feature value contains the 128 bytes of the whitened quantized embedding.
        seq_example = tf.train.SequenceExample(
            feature_lists=tf.train.FeatureLists(
                feature_list={
                    vggish_params.AUDIO_EMBEDDING_FEATURE_NAME:
                        tf.train.FeatureList(
                            feature=[
                                tf.train.Feature(
                                    bytes_list=tf.train.BytesList(
                                        value=[embedding.tobytes()]))
                                for embedding in postprocessed_batch
                            ]
                        )
                }
            )
        )
        print(seq_example)
        if writer:
            writer.write(seq_example.SerializeToString())

    if writer:
        writer.close()


    # tf.app.run()


 