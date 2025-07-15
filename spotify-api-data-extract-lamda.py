import json
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import boto3
from datetime import datetime

def lambda_handler(event, context):

    client_id= os.environ['client_id']
    client_secret= os.environ['client_secret']

    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id,
    client_secret=client_secret))
    playlist='https://open.spotify.com/playlist/5dnSFdz51E2Qouk7iFnwbl' 

    playlist_uri= playlist.split('/')[-1]
    data=sp.playlist_tracks(playlist_uri)
    
    client = boto3.client('s3')
    filename = "spotify_raw_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".json"

    client.put_object(
        Body=json.dumps(data),
        Bucket="spotify-etl-project-niladri05", 
        Key='raw_data/to_processed/' + filename
        )



