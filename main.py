import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
from bs4 import BeautifulSoup

#spotify api
client_id = '3f8620f2e92941f4be4516877c628295'
client_secret = 'b365e6d0dd2b480da783adcaf44d7795'
username_spt = 'Fausto Junior'

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=client_id,
        client_secret=client_secret,
        show_dialog=True,
        cache_path="token.txt",
        username=username_spt, 
    )
)
user_id = sp.current_user()["id"]

#date of billboard
default_url = "https://www.billboard.com/charts/hot-100/"
year_date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD ")
url_year = default_url+year_date

#extract data
response = requests.get(url_year)
website = response.text

soup = BeautifulSoup(website, "html.parser")

#get the titles
initial_title = soup.select("li ul li h3")
titles = [title.getText().strip() for title in initial_title]

#songs in spotify
song_uris = []
year = year_date.split("-")[0]
for song in titles:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

#create playlist
playlist = sp.user_playlist_create(user=user_id, name=f"{year_date} Billboard 100", public=False, description=f"Top 100 music from {year_date} playlist.")
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)