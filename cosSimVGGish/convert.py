from pydub import AudioSegment

def convert_to_wav(input_file, output_file):
    # Load the input audio file
    audio = AudioSegment.from_file(input_file)

    # Ensure the output format is WAV
    if not output_file.endswith(".wav"):
        output_file = output_file + ".wav"

    # Export the audio in WAV format
    audio.export(output_file, format="wav")

if __name__ == "__main__":
    input_file = "./trainData/14 Hits Different.m4a"  # Replace with the path to your input audio file
    output_file = "./trainData/TSwiftHitsDifferent.wav"  # Replace with the desired output file name

    convert_to_wav(input_file, output_file)
