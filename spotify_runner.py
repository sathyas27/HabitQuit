import spotipy
from spotipy.oauth2 import SpotifyOAuth

SPOTIPY_CLIENT_ID = "5bdff7528e7b4d0ebec3e0fd649a50f0"
SPOTIPY_CLIENT_SECRET = "d629b8e859eb493ca907a3fc18aa1fa0"
SPOTIPY_REDIRECT_URI = "http://127.0.0.1:8888/callback"

scope = "user-read-playback-state user-modify-playback-state"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope=scope,
    open_browser=True,
))

def play_ringa_ringa_on_active_device():
    # Find an active device (Spotify desktop open helps a lot)
    devices = sp.devices().get("devices", [])
    if not devices:
        print("No Spotify devices found. Open Spotify on your Mac and try again.")
        return

    device_id = next((d["id"] for d in devices if d.get("is_active")), devices[0]["id"])

    results = sp.search(q='track:"Ringa Ringa"', type="track", limit=1)
    items = results["tracks"]["items"]
    if not items:
        print('Could not find a track matching "Ringa Ringa".')
        return

    track_uri = items[0]["uri"]

    sp.start_playback(device_id=device_id, uris=[track_uri])