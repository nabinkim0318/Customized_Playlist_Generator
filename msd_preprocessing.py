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


# still needs to work on constructing and returning a dataframe
def preprocess_h5_info(file_path):
    try:
        with h5py.File(file_path, 'r') as file:
            # Define the path to the 'analysis' group
            analysis_group_path = '/analysis'

            # Check if the 'analysis' group exists in the file
            if analysis_group_path in file:
                # Access the 'analysis' group
                analysis_group = file[analysis_group_path]

                # Function to print datasets within the 'analysis' group
                def print_datasets_in_group(group):
                    print(f'Datasets within {group.name}:')
                    for dataset_name in group.keys():
                        dataset = group[dataset_name]
                        print(f'Dataset Name: {dataset_name}, Shape: {dataset.shape}, Dtype: {dataset.dtype}')

                # Print datasets within the 'analysis' group
                print_datasets_in_group(analysis_group)
            else:
                print(f"'analysis' group not found in {file_path}")
    except Exception as e:
        print(f"Error: {e}")

msd_dataset_directory = "/Users/soyeonhong/Downloads/MillionSongSubset/"
iterate_h5_files(msd_dataset_directory)
