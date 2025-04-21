import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from typing import Optional

from config import settings

def auth_spotify(scope: Optional[str]=None):
    """Authenticate Spotify API Connection"""
    if scope:
        auth_manager = SpotifyOAuth(
            client_id=settings.SPOTIFY_CLIENT_ID,
            client_secret=settings.SPOTIFY_SECRET,
            redirect_uri=settings.SPOTIFY_REDIRECT_URI,
            scope=scope
        )
        spotify = spotipy.Spotify(auth_manager=auth_manager)

    else:
        client_credentials_manager = SpotifyClientCredentials(
            client_id=settings.SPOTIFY_CLIENT_ID,
            client_secret=settings.SPOTIFY_SECRET,
        )
        spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    
    return spotify

def get_playlists():
    """Get all public playlists from a user"""

    # Authenticate Spotify
    spotify = auth_spotify()
    user_id = settings.SPOTIFY_USER_ID

    # Retrieve all playlists
    offset = 0
    all_playlists = []
        
    while True:
        playlists = spotify.user_playlists(user_id, offset=offset, limit=30)
        all_playlists.extend(playlists["items"])

        if not playlists["next"]:
            break  # No more pages

        offset += 30  # Move to the next page

    return all_playlists

def get_device(spotify):
    devices = spotify.devices().get("devices", [])
    for device in devices:
        if device["is_active"]:
            return device

# def play_track(spotify, track_name):



if __name__ == "__main__":
    playlists = get_playlists()

    print("Playlists")
    for playlist in playlists:
        print(playlist["name"])
        # print(f"Playlist Name: {playlist['name']}, ID: {playlist['id']}")





