from __future__ import print_function
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, './audioset/vggish'))
import vggish_slim
import vggish_params
import vggish_input
import vggish_postprocess
import tensorflow.compat.v1 as tf
tf.compat.v1.disable_eager_execution()
import soundfile as sf
import numpy as np

sess = tf.compat.v1.Session()

def CreateVGGishNetwork(hop_size=0.96):   # Hop size is in seconds.
  """Define VGGish model, load the checkpoint, and return a dictionary that points
  to the different tensors defined by the model.
  """
  vggish_slim.define_vggish_slim()
  checkpoint_path = './audioset/vggish/vggish_model.ckpt'
  vggish_params.EXAMPLE_HOP_SECONDS = hop_size
  vggish_slim.load_vggish_slim_checkpoint(sess, checkpoint_path)
  features_tensor = sess.graph.get_tensor_by_name(
      vggish_params.INPUT_TENSOR_NAME)
  embedding_tensor = sess.graph.get_tensor_by_name(
      vggish_params.OUTPUT_TENSOR_NAME)
  layers = {'conv1': 'vggish/conv1/Relu',
            'pool1': 'vggish/pool1/MaxPool',
            'conv2': 'vggish/conv2/Relu',
            'pool2': 'vggish/pool2/MaxPool',
            'conv3': 'vggish/conv3/conv3_2/Relu',
            'pool3': 'vggish/pool3/MaxPool',
            'conv4': 'vggish/conv4/conv4_2/Relu',
            'pool4': 'vggish/pool4/MaxPool',
            'fc1': 'vggish/fc1/fc1_2/Relu',
            #'fc2': 'vggish/fc2/Relu',
            'embedding': 'vggish/embedding',
            'features': 'vggish/input_features',
         }
  g = tf.get_default_graph()
  for k in layers:
    layers[k] = g.get_tensor_by_name( layers[k] + ':0')
  return {'features': features_tensor,
          'embedding': embedding_tensor,
          'layers': layers,
         }
  
def ProcessWithVGGish(vgg, x, sr):
  '''Run the VGGish model, starting with a sound (x) at sample rate
  (sr). Return a whitened version of the embeddings. Sound must be scaled to be
  floats between -1 and +1.'''
  # Produce a batch of log mel spectrogram examples.
  input_batch = vggish_input.waveform_to_examples(x, sr)
  # print('Log Mel Spectrogram example: ', input_batch[0])
  [embedding_batch] = sess.run([vgg['embedding']],
                               feed_dict={vgg['features']: input_batch})
  # Postprocess the results to produce whitened quantized embeddings.
  pca_params_path = './audioset/vggish/vggish_pca_params.npz'
  pproc = vggish_postprocess.Postprocessor(pca_params_path)
  postprocessed_batch = pproc.postprocess(embedding_batch)
  # print('Postprocessed VGGish embedding: ', postprocessed_batch[0])
 # tf.reset_default_graph()
  return np.array(postprocessed_batch)

def EmbeddingsFromVGGish(vgg, x, sr):
  '''Run the VGGish model, starting with a sound (x) at sample rate
  (sr). Return a dictionary of embeddings from the different layers
  of the model.'''
  # Produce a batch of log mel spectrogram examples.
  input_batch = vggish_input.waveform_to_examples(x, sr)
  # print('Log Mel Spectrogram example: ', input_batch[0])
  layer_names = vgg['layers'].keys()
  tensors = [vgg['layers'][k] for k in layer_names]
  results = sess.run(tensors,
                     feed_dict={vgg['features']: input_batch})
  resdict = {}
  for i, k in enumerate(layer_names):
    resdict[k] = results[i]
  #tf.reset_default_graph()
  return resdict

def read_vggish_embeddings(wav_path, hop_size = 0.96):
  """LEGACY originally used to read in vggish embeddings from main.py

  Args:
      wav_path (_string_): path to wav files
      hop_size (float, optional): _description_. Defaults to 0.96.

  Returns:
      embeddings of VGGish model
  """
  sess = tf.Session()
  vgg = CreateVGGishNetwork(0.96)
  x, sr = sf.read(wav_path)
  resdict = EmbeddingsFromVGGish(vgg, x, sr)
  tf.reset_default_graph()
  # return ProcessWithVGGish(vgg, x, sr) # whitened and quantized
  return resdict["embedding"]
  
# if __name__ == "__main__":
#     # sess = tf.Session()
#     # vgg = CreateVGGishNetwork(0.96)
#     # x, sr = sf.read("/Users/leksa/Documents/GATECH/MUSI 6201 Audio Content Analysis/Project/Customized_Playlist_Generator/cosSimVGGish/trainData/01-D_AMairena.wav")
#     # print(ProcessWithVGGish(vgg, x, sr))
    
#   a = read_vggish_embeddings("/Users/leksa/Documents/GATECH/MUSI 6201 Audio Content Analysis/Project/Customized_Playlist_Generator/cosSimVGGish/trainData/Skrillex - Bangarang (Ft. Sirah) [Official Audio].wav")
  
#   print(a)