#-------------------------------------------------------------------------------
# Name:        Audio Management
# Purpose:     To convert audio files into the preferred format.
# Dependancies: ffmpeg
# Author:      Benanas
# Created:     03-15-2023
#-------------------------------------------------------------------------------

from pydub import AudioSegment
import soundfile as sf
import os

# # Set the directory where your .flac / .aif / .m4a files are stored
input_directory = r'F:\Google Drive\BenFerence\Downloads'
#input_directory = r'M:\Dropbox (Professional DJ team)\Danceworks2024\Edits\StPhilip'

# # Define function that will convert your .flac files.
def convert_flac_aif():

    # # Load the flac file using pydub
    flac_path = os.path.join(dirpath, filename)
    audio = AudioSegment.from_file(flac_path, format='flac')

    # # Define the output file path and save the converted audio
    output_path = os.path.join(dirpath, os.path.splitext(filename)[0] + '.aif')
    audio.export(output_path, format='aiff')
    print(f'"{filename}" successfully converted to AIF')

    # # Delete the original flac file
    os.remove(flac_path)


# # Define function that will convert your .wav files.
def convert_wav_aif():

    # # Load the fwav file using soundfile
    wav_path = os.path.join(dirpath, filename)
    data, samplerate = sf.read(wav_path)

    # # Define the output file path and save the converted audio
    output_path = os.path.join(dirpath, os.path.splitext(filename)[0] + '.aif')
    sf.write(output_path, data, samplerate, format='aiff',subtype='PCM_16')
    print(f'"{filename}" successfully converted to AIF')

    # # Delete the original wav file
    os.remove(wav_path)


# # Define function that will convert your .m4a files.
def convert_m4a_aif():

    # # Load the m4a file using pydub
    m4a_path = os.path.join(dirpath, filename)
    audio = AudioSegment.from_file(m4a_path, format='m4a')

    # # Define the output file path and save the converted audio
    output_path = os.path.join(dirpath, os.path.splitext(filename)[0] + '.aiff')
    audio.export(output_path, format='aiff')
    print(f'"{filename}" successfully converted to AIF')

    # # Delete the original m4a file
    os.remove(m4a_path)


if __name__ == '__main__':

    # # Loop through all files in the directory
    for dirpath, dirnames, filenames in os.walk(input_directory):
        for filename in filenames:

            try:
                if filename.endswith('.wav'):
                    convert_wav_aif()

                if filename.endswith('.flac'):
                    convert_flac_aif()

                if filename.endswith('.m4a'):
                    convert_m4a_aif()

            except Exception as e:
                print(f'Error converting {filename}: {e}')