## Import beautifulSoup for web Scrapping, Spotipy for acessing Spotify API
from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import secret


## Ask the user to input date so that the songs can be scrapped of that date.
date = input("Which Year do you want to travel to? Type in the date in this format YYYY-MM-DD:")

## Scrapping the titles of the songs of that particular day and storing them in a list.
contents = requests.get("https://www.billboard.com/charts/hot-100/"+date)
soup = BeautifulSoup(contents.text, "html.parser")
song_span = (soup.select("li ul li h3", class_="c-title"))
songs = []
for i in song_span:
    songs.append(i.text.strip())


## Authorizing Spotify to create a playlist of the songs by fetching them using Spotify API
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri=secret.redirect_uri,
        client_id=secret.client_id,
        client_secret=secret.client_secret,
        show_dialog=True,
        cache_path=secret.cache_path
    )
)
year = date[:4]
songs_uri=[]
user_id = sp.current_user()['id']

##Creating the playlist
for song in songs:
    try:
        res = sp.search(q=f"track:{song} year:{year}", type="track")['tracks']['items'][0]['uri']
        songs_uri.append(res)
    except:
        print(f'{song} is not available on Spotify. Skipped!')

playlist = sp.user_playlist_create(user=user_id, name=f'{date} Billboard 100', public=False)


sp.playlist_add_items(playlist_id=playlist['id'], items=songs_uri)

print("CONGRATULATIONS! YOU HAVE CREATED THE PLAYLIST!!!")



    



