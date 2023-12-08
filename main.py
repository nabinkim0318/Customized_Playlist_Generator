import pandas as pd
import sys
import os
import subprocess
import shutil
import high_level_input
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

def playlist_generate(high_level = "evaluation_random", method=ALL_METHODS):
        # first convert all files into wav
    convert.convert_folder_to_wav(SEED_SONG_FOLDER)
    
    counter = 0
    if counter == 0:
        working_directory = "./similarity"
        os.chdir(working_directory)
        subprocess.run(["python3", "similarity_main.py"])
        counter += 1
    vgg = vggish_embeddings.CreateVGGishNetwork(vggish_window)
    if high_level == "similarity":
        high_level_input.similarity_based_main()
        result_report = get_playlist_report_reorganize_folders(method=method, vgg=vgg, high_level =high_level+"_based")
    if high_level == "random":
        high_level_input.random_main()
        result_report = get_playlist_report_reorganize_folders(method=method, vgg=vgg, high_level=high_level+"_songs")
    if high_level.split("_")[0] == "evaluation":
        
        convert.convert_folder_to_wav("../song_data/")
        if high_level.split("_")[1] == "similarity":
            high_level_input.copy_wav_files(source_folder="../song_data/seed_songs/", destination_folder="../song_data/similarity_based")
            result_report = get_playlist_report_reorganize_folders(method=method, vgg=vgg, high_level="similarity_based", seed_song_folder="song_data")
            result_report.to_csv("../eval/similarity_based_luhee_top5.csv",index=False)
        if high_level.split("_")[1] == "random":
            high_level_input.copy_wav_files(source_folder="../song_data/seed_songs/", destination_folder="../song_data/random_songs")
            result_report = get_playlist_report_reorganize_folders(method=method, vgg=vgg, high_level="random_songs", seed_song_folder="song_data")
            result_report.to_csv("../eval/random_songs_luhee_top5.csv",index=False)

    # iterate through each song



    print("hi")           
                
                
                
            
            
            #print(dir)
            
    

    return 

def get_playlist_report_reorganize_folders(method, vgg, high_level="similarity_based", seed_song_folder=SEED_SONG_FOLDER):
    seed_song_names_col = []
    folder_names = []
    methods_col = []
    output_song_col = []
    if seed_song_folder == "song_data":
        song_subset_folder = os.path.join("..", seed_song_folder, high_level)
    else:
        song_subset_folder = os.path.join("..", SEED_SONG_FOLDER, "input",high_level)
    
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
            if seed_song_folder == "song_data":
                output_dir = os.path.join("..", seed_song_folder, "output", m, high_level, drctry)
            else:
                output_dir = os.path.join("..", SEED_SONG_FOLDER, "output",m, high_level, drctry)
            # output_dir = os.path.join("..",SEED_SONG_FOLDER, "output", m, drctry)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            output_songs = list(sim_matrix["name"][1:TOP_N+1])
            output_songs = [name.replace(".wav", ".mp3") for name in output_songs]
            output_song_col += output_songs
            for song in tqdm(output_songs):
                if os.path.exists(output_dir):
                    shutil.copy(os.path.join( current_folder_name_for_method, song), os.path.join( output_dir, song))
                else:
                    print(f"Output directory: {output_dir} does not exist!")
    
    result_report = pd.DataFrame({"Seed_song_names": seed_song_names_col, "Similarity_method": methods_col, "All_songs": output_song_col})
    return result_report
        

if __name__ == "__main__":
    playlist_generate()