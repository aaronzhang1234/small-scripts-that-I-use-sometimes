import json
from pymongo import MongoClient

client = MongoClient(port=27017)
db = client.heartbeat

def get_playlist_tracks():
    f = open("playlisttracks.json")
    data = json.load(f)

    items = data["items"]

    for item in items:
        item["_id"] = item["track"]["id"]
        if db.tracks.find_one({"_id":item["_id"]}) == None:
            result = db.tracks.insert_one(item)
            print(result)
        print(item["track"]["id"], end=",")

def get_track_tempos():
    f = open("audiofeatures.json")
    data = json.load(f)
    
    items = data["audio_features"]
    audio_dict = dict()
    for item in items:
        item["_id"] = item["id"] 
        if db.audiofeature.find_one({"_id":item["id"]}) == None:
            result = db.audiofeature.insert_one(item)
            print(result)
        audio_dict[item["id"]] = item["tempo"]

    sorted_dict = dict(sorted(audio_dict.items(), key=lambda item: item[1]))
    print(sorted_dict)



if __name__ == "__main__":
    get_track_tempos()
    #get_playlist_tracks()
