import os
import subprocess

def convert_folder_to_wav(input_folder):
    for foldername, subfolders, filenames in os.walk(input_folder):
        for filename in filenames:
            if filename.lower().endswith((".mp3", ".ogg", ".flac")):
                input_file_path = os.path.join(foldername, filename)
                output_file_path = os.path.splitext(input_file_path)[0] + ".wav"
                if not os.path.exists(output_file_path):
                    subprocess.run(["ffmpeg", "-i", input_file_path, output_file_path])

                    print(f"Converted: {input_file_path} to {output_file_path}")

