# Important scripts that I may use sometimes when it is necessary

## makefolders.sh

### For those who prefer being complicated

To make your computer a labyrinth that no one can navigate, use this bash script to create 100 folders in the current directory with their only form of identification being a number between 1 and 100.

Perfect for hiding your documents when no one around you knows how to use grep or anyother commands.

## synchronize.py and synchronizeEx.json

### Keeping backups without needing the internet

I have a USB drive which I keep some of my most valuable files on it. 

-School Labs

-Academic Papers

-Useful, Portable Code

-Memes

That being said, it's very hard and annoying to copy and paste everything using finder and guis. So I made this to simplify the task.

In synchonizeEx.json, folder1 is the source folder while folder2 is the destination folder. I made a time value so that it'll only copy items made after the last copy, don't worry about putting some arbitrary time at first, just put the folders in and you'll be good.

## metCrawler.py

### Knowledge is power, but also is showing people your collection of 400 art related books

Inspired by [dataslap's post](https://news.ycombinator.com/item?id=16303046) on news.ycombinator.com, I decided to make my own scrapy bot to download the 22 gigabyte treasure trove that the MET released.

This file is only the bot through, to actually use the bot you will have to follow the instructions on http://scrapy.org to create the file structure, then simply copy and pasting the code into your main spider file and running

`scrapy crawl metCrawler`

Will begin the processs, **however** make sure to change the directory in line 23 to the location you want your pdfs to be stored. 

dataslap's code found on the site is much better than mine, but I just learned how to use scrapy just yesterday and this was a fun little project to do.
