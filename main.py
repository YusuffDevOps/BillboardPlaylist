from bs4 import BeautifulSoup
import requests, spotipy
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint
from dotenv import load_dotenv
import os

load_dotenv()

URL = "https://www.billboard.com/charts/hot-100"
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
REDIRECT_URI = "https://www.billboard.com/charts/hot-100/"
scope = os.environ.get("scope")
date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
response = requests.get(url=f"{URL}/{date}")
website_html = response.text

soup = BeautifulSoup(website_html, "html.parser")
song_tags = soup.select(selector="li .c-title")
artist_tags = soup.select(selector="span.a-no-trucate")
song_names = [tag.getText().strip() for tag in song_tags]
artist_names =  [tag.getText().strip() for tag in artist_tags]
# print(song_names)
# print(artist_names)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_secret=CLIENT_SECRET,
                                               client_id=CLIENT_ID, redirect_uri=REDIRECT_URI))
user = sp.current_user()
user_id = user["id"]
print(user_id)

song_uris = []
for song in song_names:
    new_song = sp.search(q=f"track:{song}, year:{2023}",type="track", limit=5)
    try:
        song_uris.append(new_song["tracks"]["items"][0]["uri"])
    except IndexError:
        print("Song Does not exist in Spotify")

print(song_names)

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
playlist_id = playlist["id"]


pprint(sp.playlist_add_items( playlist_id=playlist_id, items=song_uris))