import dotenv
import base64
import requests
import json

def get_token():
    client_id = dotenv.get_variable('.variables', 'CLIENT_ID')
    client_secret = dotenv.get_variable('.variables', 'CLIENT_SECRET')

    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')
    
    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': 'Basic ' + auth_base64,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {'grant_type': 'client_credentials'}
    result = requests.post(url, headers=headers, data=data)
    json_results = json.loads(result.content)
    token = json_results['access_token']
    return token

def get_auth_headers(token):
    return {'Authorization': 'Bearer ' + token}

def search_artist(token, artist_name):
    url = 'https://api.spotify.com/v1/search'
    headers = get_auth_headers(token)
    query = f'?q={artist_name}&type=artist&limit=1'
    
    query_url = url + query
    
    result = requests.get(query_url, headers=headers)
    json_results = json.loads(result.content)
    artists = json_results['artists']['items']
    
    if len(artists) == 0:
        raise Exception(f'No artists called "{artist_name}" has been found in the spotify api.')
    
    return artists[0]

def get_songs_by_artist(token, artist_id):
    url = f'https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US'
    headers = get_auth_headers(token)
    
    result = requests.get(url, headers=headers)
    json_results = json.loads(result.content)
    tracks = json_results['tracks']
    
    return tracks

def get_song_by_name(token, song_name):
    url = 'https://api.spotify.com/v1/search'
    headers = get_auth_headers(token)
    query = f'?q={song_name}&type=track&limit=1'
    
    query_url = url + query
    
    result = requests.get(query_url, headers=headers)
    json_results = json.loads(result.content)
    tracks = json_results['tracks']['items']
    
    return tracks

def get_songs_subtitles(song_id):
    url = f'https://spotify-lyric-api.herokuapp.com/?trackid={song_id}'
    
    result = requests.get(url)
    json_results = json.loads(result.content)
    
    if(json_results['error'] == True):
        raise Exception(json_results['message'])
    
    if(json_results['syncType'] == 'UNSYNCED'):
        print('Time codes are not synced. Be careful when using it')
    
    return json_results