import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from bs4 import BeautifulSoup
import pprint

global playlist_id
SPOTIFY_ENDPOINT = "https://api.spotify.com/v1/search"
# SPOTIPY_CLIENT_ID = "51a56a732afe4fd89e915ce6de1c99be"
# SPOTIPY_CLIENT_SECRET = "de0699aedfa746d8935bf06fb5d5124b"

date = str(input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: "))

response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}/")
webpage_html = response.text
soup = BeautifulSoup(webpage_html, "html.parser")
title = soup.select(selector="li ul li h3")
final_list = [item.string.strip() for item in title]

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

tracks =[]
for item in final_list:
    result = spotify.search(item, type="track")
    albums = result["tracks"]["items"][0]
    tracks.append(albums["uri"])

pp = pprint.PrettyPrinter()
scope = "playlist-modify-private"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
user_uri_id = sp.current_user()["uri"]
user_id = sp.current_user()["id"]

name = f"{date} Billboard 100"
playlist_new = sp.user_playlist_create(user_id, name, public=False, description="description")
print(playlist_new)
# scope = "playlist-read-private"
# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
# user_playlists = sp.user_playlists(user_id)
#
# scope = "playlist-modify-private playlist-modify-public"
# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
# for playlist in user_playlists["items"]:
#     if str(playlist["name"]) == str(name):
#         playlist_id = playlist["id"]
#         print(playlist_id)

for item in tracks:
    sp.playlist_add_items(playlist_id, [f"{item}"])