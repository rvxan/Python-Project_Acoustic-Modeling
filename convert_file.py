from pydub import AudioSegment
import wave
import os


def convert_to_wav(input_file, output_file):
    # Check the input file format
    input_format = input_file.split('.')[-1].lower()

    if input_format == 'wav':
        print("Input file is already in WAV format. No conversion needed.")
        return
    elif input_format in ('mp3', 'aac'):
        # Load the audio from the input file
        audio = AudioSegment.from_file(input_file, format=input_format)

        # Export the audio to WAV format
        audio.export(output_file, format="wav")

        print("Conversion to WAV successful.")
    else:
        print(f"Unsupported input file format: {input_format}")


if __name__ == "__main__":
    input_file = "ist_clap2.mp3"  # Replace with your input file
    output_file = "ist_clap2.mp3"  # Replace with your output file

    try:
        convert_to_wav(input_file, output_file)
    except Exception as e:
        print(f"Error: {e}")