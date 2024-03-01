#-------------------------------------------------------------------------------
# Name:        Filename Cleaner
# Purpose:     To convert audio files into the preferred format.
# Author:      Benanas
# Created:     03-15-2023
#-------------------------------------------------------------------------------


import os

def CleanFilename(directory, string_to_remove):
    for filename in os.listdir(directory):
        if string_to_remove in filename:
            new_filename = filename.replace(string_to_remove, '')
            old_file_path = os.path.join(directory, filename)
            new_file_path = os.path.join(directory, new_filename)
            os.rename(old_file_path, new_file_path)
            print(f'Renamed "{filename}" to "{new_filename}"')

directory_path = r'F:\Google Drive\BenFerence\Downloads'
string_to_remove = ' myfreemp3.vip '

CleanFilename(directory_path, string_to_remove)
