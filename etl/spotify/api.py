import spotipy
from spotipy.oauth2 import SpotifyOAuth


def credentials(CLIENT_ID, CLIENT_SECRET, LIMIT):
    spotify_client_id = CLIENT_ID
    spotify_client_secret = CLIENT_SECRET
    spotify_redirect_url = "http://localhost:8080"
    spotify_req_limit = LIMIT

    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=spotify_client_id,
            client_secret=spotify_client_secret,
            redirect_uri=spotify_redirect_url,
            scope="user-read-recently-played",
        )
    )  

    return sp