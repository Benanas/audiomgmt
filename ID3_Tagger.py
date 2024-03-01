#-------------------------------------------------------------------------------
# Name:        ID3 Tagger
# Purpose:     To convert audio files into the preferred format.
# Author:      Benanas
# Created:     03-15-2023
#-------------------------------------------------------------------------------

import os, musicbrainzngs, re
from mutagen.flac import FLAC
from mutagen.id3 import ID3, TPE1, TIT2, TALB, TDRC, TCON, TRCK, TYER, TXXX, ID3NoHeaderError
from mutagen.aiff import AIFF

#TIT2: Title/song name/content description
##    Mutagen
##    TPE1: Lead performer(s)/Soloist(s)
##    TALB: Album/Movie/Show title
##    TRCK: Track number/Position in set
##    TYER: Year of release
##    TCON: Content type (Genre)
##    COMM: Comments
##    TPE4: Interpreted, remixed, or otherwise modified by
##    TPUB: Publisher
##    TCOM: Composer
##    TENC: Encoded by
##    APIC: Attached picture (album art)
##    USLT: Unsynchronized lyric/text transcription
##    SYLT: Synchronized lyric/text
##    COMM: Comments
##    TXXX: User defined text information frame

################################################################################

def reset_id3_tags(filepath):

    try:
        # Load the ID3 tags from the file
        audio = ID3(filepath)
    except ID3NoHeaderError:
        print("Error: File does not contain ID3 tag header.")
        return

    # Check if there are any COMM frames and delete them
    comm_keys = [key for key in audio.keys() if key.startswith('COMM')]
    if comm_keys:
        for key in comm_keys:
            del audio[key]
        audio.save()
        print("All COMM tags have been deleted.")
    else:
        print("No COMM tags found in the file.")


def extract_vorbis_tags(file_path):
    # Attempt to open the FLAC file
    try:
        audio = FLAC(file_path)
    except Exception as e:
        print(f"Error opening file: {e}")
        return None

    # Initialize variables
    tags = {
        'artist': None,
        'year': None,
        'title': None,
        'remixer': None,
        'label': None,
        'genre': None,
        'album': None,
        'release_date': None
    }

    # Extract tags if present
    if 'artist' in audio:
        tags['artist'] = audio['artist'][0]
    if 'date' in audio:
        tags['year'] = audio['date'][0]
    if 'title' in audio:
        tags['title'] = audio['title'][0]
    if 'remixer' in audio:
        tags['remixer'] = audio['remixer'][0]
    if 'label' in audio:
        tags['label'] = audio['label'][0]
    if 'genre' in audio:
        tags['genre'] = audio['genre'][0]
    if 'album' in audio:
        tags['album'] = audio['album'][0]
    if 'release_date' in audio:
        tags['release_date'] = audio['release_date'][0]

    return tags

################################################################################
################################################################################

def apply_id3_tags_aif(file_path, artist=None, year=None, title=None, remixer=None, label=None, genre=None, album=None, release_date=None):
    try:
        audio = AIFF(file_path)

        # Attempt to add ID3 tag if it doesn't exist
        try:
            audio.add_tags()
        except ID3NoHeaderError:
            pass  # Tag exists

        # Artist
        if artist:
            audio.tags.add(TPE1(encoding=3, text=[artist]))

        # Title
        if title:
            audio.tags.add(TIT2(encoding=3, text=[title]))

        # Album
        if album:
            audio.tags.add(TALB(encoding=3, text=[album]))

        # Year and Release Date
        # For AIFF, TDRC (Recording Time) is more versatile than TYER (Year)
        if year or release_date:
            date_str = release_date or year
            audio.tags.add(TDRC(encoding=3, text=[date_str]))

        # Genre
        if genre:
            audio.tags.add(TCON(encoding=3, text=[genre]))

        # Custom tags for Remixer and Label, as there are no standard ID3 frames for these
        if remixer:
            audio.tags.add(TXXX(encoding=3, desc="REMIXER", text=[remixer]))
        if label:
            audio.tags.add(TXXX(encoding=3, desc="LABEL", text=[label]))

        audio.save()
    except Exception as e:
        print(f"Error processing file: {e}")
        return False

    return True

################################################################################
################################################################################

def audio_metadata(artist_name, song_title):
    musicbrainzngs.set_useragent("YourAppName", "0.1", "YourContactInfo")  # Replace with your app's info

    try:
        # Adjusted limit to 3 to fetch more results
        result = musicbrainzngs.search_recordings(query=f"artist:{artist_name} AND recording:{song_title}", limit=10)
    except Exception as e:
        print(f"Error searching for song: {e}")
        return None

    matches = result.get('recording-list', [])
    if matches:
        print("Here are the top matches:")
        for i, recording in enumerate(matches, 1):
            # Extracting basic info; more complex data (like remixer) might not be directly available
            artist_search = recording['artist-credit'][0]['artist']['name'] if 'artist-credit' in recording else "Unknown"
            title_search = recording.get('title', "Unknown Title")
            # Release year and remixer might need more specific handling or might not be available directly
            release_year = recording.get('release-list', [{}])[0].get('date', 'Unknown Date')[:4]  # Simplified handling of year
            print(f"{i}. Artist: {artist_search}, Title: {title_search}, Release Year: {release_year}")

        # Prompt user to choose the correct record
        choice = int(input("Please enter the number of the correct record (##): ")) - 1
        if choice < 0 or choice >= len(matches):
            print("Invalid selection.")
            return None

        # Assuming the user selects a valid option, store and return metadata of the chosen record
        chosen_recording = matches[choice]

        remixer = extract_remix_artist(chosen_recording.get('title', ""))
        print(remixer)

        remixer = extract_remixer(chosen_recording.get('title', ""))
        print(remixer)

        metadata = {
            'artist': artist_name,
            'title': song_title,
##            'artist': chosen_recording['artist-credit'][0]['artist']['name'] if 'artist-credit' in chosen_recording else "Unknown",
##            'title': chosen_recording.get('title', "Unknown Title"),
            'year': chosen_recording.get('release-list', [{}])[0].get('date', 'Unknown Date')[:4],  # Simplified handling
            'album': chosen_recording.get('title', "Unknown Album"),
            'release_date': chosen_recording.get('date', "Unknown Release Date"),
            'label': chosen_recording.get('label-info-list', [{}])[0].get('label', {}).get('name', "Unknown Label") if 'label-info-list' in chosen_recording else None,
##            'genre': "Unknown",  # Genre might require additional handling or queries to accurately determine
            'remixer': remixer  # Would require additional handling or queries to accurately determine
        }

        return metadata

    else:
        print("No matches found.")
        return None

################################################################################
################################################################################

def extract_remix_artist(title):
    """
    Extracts the remixer's name from the track title if it indicates a remix.
    Assumes the remixer's name is enclosed in parentheses or brackets and contains 'remix'.
    """
    start = title.find('(')
    end = title.find(')', start)
    if start != -1 and end != -1 and 'remix' in title[start:end].lower():
        remix_part = title[start+1:end].lower().replace(' remix', '').replace('remix', '')
        return remix_part.title()  # Capitalize the first letter of each word
    return None

################################################################################
################################################################################

def extract_remixer(title):
    # Regex pattern to match (Remix) or [Remix] patterns, case-insensitive
    pattern = r'\((.*?remix.*?)\)|\[(.*?remix.*?)\]'

    # Search for pattern in the title
    matches = re.findall(pattern, title, re.IGNORECASE)

    if matches:
        # Extract the remix artist name, remove 'remix' or 'Remix', and strip extra spaces
        for match in matches:
            remix_part = match[0] if match[0] else match[1]  # Select the non-empty match
            remix_artist = re.sub(r'\bremix\b', '', remix_part, flags=re.IGNORECASE).strip()
            return remix_artist
    return None

################################################################################
################################################################################

if __name__ == '__main__':

    # Example usage
    file_path = r'F:\Google Drive\BenFerence\Downloads\Vibe Emissions - Purple in my Cup.flac'
    tags = extract_vorbis_tags(file_path)
    print(tags)
    print(tags['title'])

    # Example usage
##    file_path = 'path/to/your/file.aif'
##    success = apply_id3_tags_to_aif(file_path, artist="Artist Name", year="2020", title="Track Title", remixer="DJ Remix", label="Label Name", genre="Genre", album="Album Name", release_date="2020-01-01")
##    if success:
##        print("Tags applied successfully.")
##    else:
##        print("Failed to apply tags.")

    # Example usage

##    metadata = audio_metadata(tags['title'], tags['artist'])
##    print(metadata)

    metadata = audio_metadata("month", "gas tank")
    print(metadata)


