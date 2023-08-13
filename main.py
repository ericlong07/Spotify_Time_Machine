from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = "ba01c666fd5e42b695db9567d66749bf"
CLIENT_SECRET = "99289b11ba4b4e049dab5bf2709dd3f0"
REDIRECT_URL = "https://example.com/callback/"

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

response = requests.get(f'https://www.billboard.com/charts/hot-100/{date}')

soup = BeautifulSoup(response.text, 'html.parser')
song_names_span = soup.find_all(name='h3', class_='a-no-trucate')
song_names = [song.getText().strip('\t\n') for song in song_names_span]

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri=REDIRECT_URL,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()['id']

song_uris = []
year = date.split('-')[0]
for song in song_names:
    result = sp.search(q=f'track:{song} year:{year}', type='track')
    print(result)
    try:
        uri = result['tracks']['items'][0]['uri']
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

new_playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
sp.playlist_add_items(playlist_id=new_playlist['id'], items=song_uris)
