import os
import eyed3

files = os.listdir('.')
for f in files:
    if f[-3:] == 'mp3':
        song = eyed3.load(f)
        if(song.tag == None):
            song.tag.initTag()
        song.tag.images.set(3, open('enigmatic.jpg', 'rb').read(), 'image/jpeg')
        song.tag.save()
