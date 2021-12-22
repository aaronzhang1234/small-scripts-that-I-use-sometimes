from pymongo import MongoClient
import json
import requests

client = MongoClient(port=27017)
db = client.heartbeat
OAUTH_TOKEN = <OAUTH_TOKEN_HERE>
headers={"Authorization":"Bearer "+OAUTH_TOKEN, "Content-Type":"application/json"}

def get_music_and_save_tracks():
    playlist_ids = get_playlist_ids()
    for playlist_id in playlist_ids:
        tracks_arr = get_playlist_tracks(playlist_id)
        while len(tracks_arr) != 0:
            tracks_arr_slice = tracks_arr[:100]
            tracks = ",".join(tracks_arr_slice)
            get_track_tempos(tracks)
            tracks_arr = tracks_arr[100:]

def get_playlist_ids():
    f = open("playlists.json")
    data = json.load(f)

    items = data["items"]
    arr = []
    for item in items:
        arr.append(item["id"])
    return arr

def get_playlist_tracks(playlist_id):
    arr = [] 
    offset=0
    still_songs = True

    while still_songs:
        r = requests.get(url="https://api.spotify.com/v1/playlists/"+playlist_id+"/tracks?offset="+str(offset), headers=headers)
        response_json = r.json()
        items = response_json["items"]
        for item in items:
            item["_id"] = item["track"]["id"]
            if db.tracks.find_one({"_id":item["_id"]}) == None:
                result = db.tracks.insert_one(item)
                print("Inserting track: " + str(item["track"]["name"]))
            arr.append(item["track"]["id"])
        if response_json["total"]<=offset+50:
            still_songs = False
        offset+=50
    return arr

def get_track_tempos(tracks):
    r = requests.get(url="https://api.spotify.com/v1/audio-features?ids="+tracks, headers=headers)
    response_json = r.json()
    
    items = response_json["audio_features"]
    audio_dict = dict()
    for item in items:
        item["_id"] = item["id"] 
        if db.audiofeature.find_one({"_id":item["id"]}) == None:
            result = db.audiofeature.insert_one(item)
            print("Inserting feature : " + str(item["id"]))

def get_track_with_closest_tempo(tempo):
    track = db.audiofeature.aggregate([
        {"$project": {"diff": {"$abs": {"$subtract": [tempo, "$tempo"]}},"doc": '$$ROOT'}},
        {"$sort": {"diff": 1}}, 
        {"$limit": 1} 
    ])
    return list(track)


if __name__ == "__main__":
    get_music_and_save_tracks()
    print(get_track_with_closest_tempo(201))
