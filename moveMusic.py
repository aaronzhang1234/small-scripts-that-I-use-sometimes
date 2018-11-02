import eyed3
import os
from os import listdir
import shutil
files = os.listdir(".")
for x in files:
    if os.path.isfile(x) and x[-3:] == 'mp3':
        audio_file = eyed3.load(x)
        album = audio_file.tag.album
        artist = audio_file.tag.artist
        if artist == 'Kan Gao' or artist == 'Laura Shigihara, arranged by Kan Gao':
            if album == 'Finding Paradise <OST>':
                shutil.move(x, '../FindingParadise/'+x)
                print(album);
                print(x)
            else:
                shutil.move(x, '../ToTheMoon/'+x)
