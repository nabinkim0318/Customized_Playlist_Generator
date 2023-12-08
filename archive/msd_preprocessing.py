import os
import pandas as pd
import h5py


def iterate_h5_files(msd_dataset_directory, h5_dataset_output_csv_directory):
    count = 0
    df_list = []
    # recursively explore the contents of a directory and its subdirectories. 
    for root, _, files in os.walk(msd_dataset_directory):
        for filename in files:
            if filename.endswith('.h5'):
                file_path = os.path.join(root, filename)
                df = preprocess_h5_info(file_path)
                if df is not None:
                    df_list.append(df)
                    count += 1
    if df_list:
        concatenated_df = pd.concat(df_list, ignore_index=True)
        concatenated_df.to_csv(h5_dataset_output_csv_directory, index=False)
        print(f"Processed and saved the cumulative results to {h5_dataset_output_csv_directory}.")
    else:
        print("No HDF5 files found or no data to save.")
    print(count)
    return concatenated_df


# still needs to work on constructing and returning a dataframe
def preprocess_h5_info(file_path):
    try:
        with h5py.File(file_path, 'r') as file:
            # information is under analysis structure 
            analysis_group_path = '/analysis'

            # Check if the 'analysis' group exists in the file
            if analysis_group_path in file:
                analysis_group = file[analysis_group_path]

                # only collecting numeric features at this moment 
                if 'songs' in analysis_group:
                    songs_dataset = analysis_group['songs']
                    songs_data = songs_dataset[0]  
                    
                    songs_dict = {}
                    for field_name in songs_data.dtype.fields:
                        field_value = songs_data[field_name]
                        songs_dict[field_name] = field_value
                    df = pd.DataFrame([songs_dict])
                    
                    return df
            else:
                print(f"'analysis' group not found in {file_path}")
    except Exception as e:
        print(f"Error: {e}")



msd_dataset_directory = "/Users/soyeonhong/Downloads/MillionSongSubset/"
h5_dataset_output_csv_directory = "/Users/soyeonhong/Downloads/h5_dataset.csv"
concatenated_df = iterate_h5_files(msd_dataset_directory, h5_dataset_output_csv_directory)
