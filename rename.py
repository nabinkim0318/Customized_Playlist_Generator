import os
import csv

def rename_files_with_mapping(folder_path, csv_file_path):
    # Read the CSV file and create a mapping dictionary
    mapping = {}
    with open(csv_file_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            mapping[row['old']] = row['new']

    # Iterate through the folder structure
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(".mp3"):
                original_path = os.path.join(root, file)
                base_name, extension = os.path.splitext(file)
                
                # Check if the file name is in the mapping
                if base_name in mapping:
                    new_base_name = mapping[base_name]
                    new_file_name = new_base_name + extension
                    new_path = os.path.join(root, new_file_name)
                    
                    # Rename the file
                    os.rename(original_path, new_path)
                    print(f"Renamed: {file} to {new_file_name}")

# Example usage
folder_path = "./song_data/random_songs/"
csv_file_path = "./mapping.csv"

rename_files_with_mapping(folder_path, csv_file_path)
