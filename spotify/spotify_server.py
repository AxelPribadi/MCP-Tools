from mcp.server.fastmcp import FastMCP
from spotify_functions import *


mcp = FastMCP("Spotify Assistant")
spotify = auth_spotify("user-read-playback-state user-modify-playback-state")

@mcp.tool()
def playback_controller(action: str,):
    """Control Spotify playback: play, pause resume, skip, previous, and queue"""

    # Get Device ID
    device = get_device(spotify)
    device_id = device["id"]

    # Select Control Action
    if action == "play":
        print("")
        return
    
    elif action == "pause":
        spotify.pause_playback(device_id)
        print(f"Paused playback on device {device["name"]}")
        return
    
    elif action == "resume":
        spotify.start_playback(device_id)
        print(f"Resumed playback on device {device["name"]}")
        return
    
    elif action == "skip":
        spotify.next_track(device_id)
        print(f"Skipped playback on device {device["name"]}")
        return
    
    elif action == "previous":
        spotify.previous_track(device_id)
        print(f"Skipped to previous playback on device {device["name"]}")
        return
    
    elif action == "queue":
        print("Added {track} to queue")
    
    else:
        print("Not a playback control")
        return device

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
