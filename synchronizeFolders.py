from shutil import copy
from multiprocessing import Process
from pprint import pprint
import json
import threading
import sys
import itertools
import os.path, time
import datetime
import os

done = False

def animate():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\rloading ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\rDone!     ')
    exit()

def printtree(src, dest, lastTime, layers):
    for item in os.listdir(src):
        s = os.path.join(src, item)   
        if layers:
            loc = s.split("/")            
            absLayers = layers+1
            loc = loc[-absLayers:]
            loc = loc[:-1]
            finishedPath = '/'.join(loc)
            v = os.path.join(dest,finishedPath)
        else:
            v = dest
        sAbsPath = os.path.abspath(s) 
        vAbsPath = os.path.abspath(v) 
        pathExists = os.path.exists(vAbsPath)
        pathIsDir = os.path.isdir(sAbsPath)
        if(pathIsDir):
            vAbsPath = vAbsPath+'/'+item
            pathExists = os.path.exists(vAbsPath)
            if not pathExists:
                os.makedirs(vAbsPath)
            printtree(s, dest, lastTime, layers+1)
        else:
            t = os.path.getmtime(sAbsPath)
            if(lastTime <= t):
                copy(sAbsPath, vAbsPath)         
      
if __name__ == "__main__":
    t = threading.Thread(target=animate)
    t.start()
    with open("synchronizeEx.json","r") as jsonFile:
       json_data = open("synchronizeEx.json").read()
    data = json.loads(json_data)
    for key in data["folders"]:
        if not 'time' in key:
            lastTime = 0
        else:
            lastTime = key["time"]
        printtree(key["folder1"], key["folder2"], lastTime, 0)
        key["time"] = int(time.time())
    with open("synchronizeEx.json","w") as jsonFile:
        json.dump(data, jsonFile, sort_keys=True, indent = 4)
    done = True

