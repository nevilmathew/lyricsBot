from lyricsgenius import Genius
from dotenv import load_dotenv
import os
def lyrics(artist,name):
    load_dotenv()
    TOKEN = os.getenv('client_access_token')
    genius = Genius(TOKEN)
    song = genius.search_song(name, artist)
    return song.lyrics