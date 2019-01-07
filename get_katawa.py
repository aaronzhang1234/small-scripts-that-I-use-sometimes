from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import urllib.request as urllib2
from pydub import AudioSegment

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--mute-audio")
driver = webdriver.Chrome(chrome_options = chrome_options)
driver.get("http://katawashoujo.wikia.com/wiki/Music")
songs = driver.find_elements_by_xpath('//ol/li')   
ogg_players = driver.find_elements_by_xpath('//div[@class="ogg_player"]/div/button')
for song in songs:
    fuck_button = song.find_element_by_xpath('.//div/div/button')
    fuck_button.send_keys('\n')
    time.sleep(1)
    audio = song.find_element_by_xpath('.//div/div/audio')
    song_link_url = audio.get_attribute('src')
    song_name = (song.text.replace("More…","")).strip()
    song_name = song_name.split(' -', 1)[0]
    print("working on " + song_name)
    ogg_katawa = urllib2.urlopen(song_link_url)
    with open(song_name+'.ogg', 'wb') as download_song:
        download_song.write(ogg_katawa.read())
    ogg_audio = AudioSegment.from_file(song_name+'.ogg', format="ogg")
    ogg_audio.export(song_name+'.mp3', format='mp3')
#song_links = driver.find_elements_by_xpath('//ol/li')   
#for song_link in song_links:
#    print(song_link.text)
#    song_link_url = song_link.get_attribute("src")
driver.close()
