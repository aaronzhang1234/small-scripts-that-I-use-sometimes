from pydub import AudioSegment
import os
from os import listdir

files = os.listdir('.')

for f in files:
    if f[-3:] == 'ogg':
        print(f[:-4])
        ogg_audio = AudioSegment.from_file(f, format="ogg")
        ogg_audio.export(f[:-4]+'.mp3', format = 'mp3')
        
