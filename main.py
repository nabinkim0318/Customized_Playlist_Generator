import pandas as pd
import sys
import os
import subprocess
import shutil
sys.path.append("./similarity/")
import config
import convert
import similarity_main
import vggish_embeddings
from tqdm import tqdm

vggish_window = config.VGGISH_WINDOW
SEED_SONG_FOLDER = config.SEED_SONG_FOLDER
ALL_METHODS = config.ALL_METHODS
TOP_N = config.TOP_N

def playlist_generate(high_level = "similarity", method=ALL_METHODS):
    
    # first convert all files into wav
    convert.convert_folder_to_wav(SEED_SONG_FOLDER)
    
    counter = 0
    if counter == 0:
        working_directory = "./similarity"
        os.chdir(working_directory)
        subprocess.run(["python3", "similarity_main.py"])
        counter += 1
    vgg = vggish_embeddings.CreateVGGishNetwork(vggish_window)
    # iterate through each song
    seed_song_names_col = []
    folder_names = []
    methods_col = []
    output_song_col = []
    if high_level == "similarity":
        song_subset_folder = os.path.join("..", SEED_SONG_FOLDER, "similarity_based/")
        # looking into each seed song subfolder

        for drctry in tqdm([entry.name for entry in os.scandir(song_subset_folder) if entry.is_dir()]):
            
            current_seed_song_name = drctry+".wav"
            seed_song_names_col += [current_seed_song_name] * len(method) * TOP_N
            current_folder_name_for_method = os.path.join(song_subset_folder, drctry)
            folder_names += [current_folder_name_for_method]


            print(current_seed_song_name)
            print(f"METHOD LIST: {method}")
            sim_dict = similarity_main.similarity(vgg=vgg,seed_song=current_seed_song_name, folder_path = current_folder_name_for_method, method=method)
            
            for m, sim_matrix in tqdm(sim_dict.items()):
                methods_col += [m] * TOP_N
                output_dir = os.path.join("..",SEED_SONG_FOLDER, "output", m, drctry)
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                output_songs = list(sim_matrix["name"][1:TOP_N+1])
                output_song_col += output_songs
                for song in tqdm(output_songs):
                    if os.path.exists(output_dir):
                        shutil.copy(os.path.join( current_folder_name_for_method, song), os.path.join( output_dir, song))
                    else:
                        print(f"Output directory: {output_dir} does not exist!")
    print(f"seed song: {len(seed_song_names_col)}, method: {len(methods_col)}, song: {output_song_col}")
    result_report = pd.DataFrame({"Seed song names": seed_song_names_col, "Similarity method": methods_col, "Recommended song": output_song_col})
    
    print(result_report)
                
                
                
                
            
            
            #print(dir)
            
    

    return 


if __name__ == "__main__":
    playlist_generate()