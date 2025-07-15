import json
import boto3
import io
import pandas as pd
from datetime import datetime


def artist(data):
    artist_list = []
    for row in data['items']:
        for key, value in row.items():
            if key=='track':
                for artist in value['artists']:
                    artist_dict = {'artist_id':artist['id'], 'artist_name':artist['name'], 'external_url': artist['href']}
                    artist_list.append(artist_dict)
    return artist_list

def album(data):
    album_list = []
    for row in data['items']:
        album_id=row['track']['album']['id']
        album_release_date= row['track']['album']['release_date']
        album_track_name=row['track']['name']
        artist_name=row['track']['artists'][0]['name']
        total_tracks= row['track']['album']['total_tracks']
        album_type=row['track']['album']['album_type']
        
        album_elements = {
        'album_id': album_id,
        'release_date': album_release_date,
        'track_name': album_track_name,
        'artist_name': artist_name,
        'total_tracks': total_tracks,
        'album_type': album_type
        }
        album_list.append(album_elements)
    return album_list

def song(data):
    song_list = []
    for row in data['items']:
        song_id = row['track']['id']
        song_name = row['track']['name']
        song_duration = row['track']['duration_ms']
        song_url = row['track']['external_urls']['spotify']
        song_popularity = row['track']['popularity']
        song_added = row['added_at']
        album_id = row['track']['album']['id']
        artist_id = row['track']['album']['artists'][0]['id']
        song_element = {'song_id':song_id,'song_name':song_name,'duration_ms':song_duration,'url':song_url,
                        'popularity':song_popularity,'song_added':song_added,'album_id':album_id,
                        'artist_id':artist_id
                    }
        song_list.append(song_element)
    return song_list



def lambda_handler(event, context):
   
    s3 = boto3.client("s3")
    bucket = "spotify-etl-project-niladri05"
    key = "raw_data/to_processed/"

    contents = s3.list_objects(Bucket=bucket, Prefix=key)['Contents']
    
    spotify_data = []
    spotify_keys = []
    for file in contents:
        if file['Key'].split('.')[-1] == 'json':
            response = s3.get_object(Bucket=bucket, Key=file['Key'])
            content=response['Body']
            jsonObject = json.loads(content.read())
            spotify_data.append(jsonObject)
            spotify_keys.append(file['Key'].split('/')[-1])


    for data in spotify_data:
        album_list = album(data)
        artist_list = artist(data)
        song_list = song(data)
        #print(album_list)
        
        #print(spotify_keys)

    
    album_df=pd.DataFrame.from_dict(album_list)
    artist_df=pd.DataFrame.from_dict(artist_list)
    song_df=pd.DataFrame.from_dict(song_list)

    album_df = album_df.drop_duplicates(subset=['album_id'])
    artist_df = artist_df.drop_duplicates(subset=['artist_id'])
    song_df = song_df.drop_duplicates(subset=['song_id'])

    album_df['release_date']= pd.to_datetime(album_df['release_date'])
    song_df['song_added']= pd.to_datetime(song_df['song_added'])

    song_key="transformed_data/songs_data/songs_transformed_" + str(datetime.now()) + ".csv"
    album_key="transformed_data/album_data/album_transformed_" + str(datetime.now()) + ".csv"
    artist_key="transformed_data/artist_data/artist_transformed_" + str(datetime.now()) + ".csv"

    song_buffer = io.StringIO()
    album_buffer = io.StringIO()
    artist_buffer = io.StringIO()

    song_df.to_csv(song_buffer, index=False) 
    song_content=song_buffer.getvalue()
    s3.put_object(Bucket=bucket, Key=song_key, Body=song_content)

    album_df.to_csv(album_buffer, index=False)
    album_content=album_buffer.getvalue()
    s3.put_object(Bucket=bucket, Key=album_key, Body=album_content)

    artist_df.to_csv(artist_buffer, index=False)
    artist_content=artist_buffer.getvalue()
    s3.put_object(Bucket=bucket, Key=artist_key, Body=artist_content)

   

#Copy data from to_processed to already_processed
    for key in spotify_keys:
        copy_source = {'Bucket': bucket, 'Key':'raw_data/to_processed/'}
        s3.copy_object(CopySource=copy_source, Bucket=bucket, Key='raw_data/already_processed/'+ key.split('/')[-1])
        #delete the json file from to_processed folder
        s3.delete_object(Bucket=bucket, Key='raw_data/to_processed/'+key.split('/')[-1])
    


            
        
            
        
