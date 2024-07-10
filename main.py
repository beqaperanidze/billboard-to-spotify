import webbrowser
import os
from dotenv import load_dotenv

from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
client_redirect = "http://example.com/callback"

date = input("Input the time you want your playlist from (YYYY-MM-DD): ")

response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}")
wb_link = response.text

soup = BeautifulSoup(wb_link, "html.parser")

song = soup.find("h3", id="title-of-a-story",
                 class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 u-font-size-23@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-245 u-max-width-230@tablet-only u-letter-spacing-0028@tablet")
songs = soup.findAll("h3", id="title-of-a-story",
                     class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only")


final_list = [song.getText().strip()]
for song in songs:
    final_list.append(song.getText().strip())

scope = 'playlist-modify-public'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=client_redirect,
                                               scope=scope))

user_id = sp.current_user()['id']

playlist_name = "Playlist from " + date
playlist_description = "Time Capsule"
playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=True, description=playlist_description)


def search_song_by_name(song_name):
    results = sp.search(q=song_name, type='track', limit=10)
    tracks = results['tracks']['items']
    for track in tracks:
        if track['name'].lower() == song_name.lower():
            return track['uri']
    return None


url_list_songs = []
for song in final_list:
    if search_song_by_name(song) is not None:
        curr_song = search_song_by_name(song)
        sp.playlist_add_items(playlist_id=playlist["id"], items=[curr_song], position=None)
