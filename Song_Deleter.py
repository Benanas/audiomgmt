#-------------------------------------------------------------------------------
# Name:        Song Deleter
# Author:      Benanas
# Created:     03-01-2024
#-------------------------------------------------------------------------------

import os
delete_dir = r"C:\Users\Benanas\Desktop\RB_DELETE"
find_dir = r"M:\Dropbox (Professional DJ team)\rekordbox"

def delete_songs(delete_dir, find_dir):
    for dirpath, dirnames, filenames in os.walk(delete_dir):
        delete_list = filenames

    for dirpath, dirnames, filenames in os.walk(find_dir):
        for filename in filenames:
            for item in delete_list:

                try:
                    if filename == item:
                            os.remove(os.path.join(dirpath, filename))
                            print("DELETED --" + os.path.join(dirpath, filename))

                            os.remove(os.path.join(delete_dir, item))
                            print("DELETED --" + os.path.join(delete_dir, item))

                except:
                    print("ERROR --" + os.path.join(dirpath, filename))

if __name__ == '__main__':
    delete_songs(delete_dir, find_dir)