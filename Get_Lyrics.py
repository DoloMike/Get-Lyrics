'''
Michael Roberts
1-17-2015
Get_Lyrics.py

Takes an audio file path as an argument,
retrieves lyrics from genius.com and
saves them to text file.
'''

import sys, urllib2, HTMLParser
from bs4 import BeautifulSoup
from mutagen import File

#replace windows default '\'s with '/'s bc that's what python likes
fileName = '/'.join((sys.argv)[1].split('\\'))

#get the folder path and remove the file name (for saving the text file later)
s=''
saveFileName = fileName.split('/')
for x in xrange(len(saveFileName)-1):
	s = s + str(saveFileName[x]) + "/"
saveFileName = s

#get the artist name and song name from the audio file metadata
audiofile = File(fileName)
tags = audiofile.tags
for tag in tags:
	if tag == 'aART':
		artist = str(tags[tag])
	elif tag[-3:] == 'nam':
		song = str(tags[tag])

#format python's weird unicode output (probably a better way to do this, I'm not sure)
artist = (artist.strip('[]')[1:]).strip("''")
saveArtist = artist

#format the artist for the genius.com url (replace spaces with '-'s)
artist = '-'.join(artist.split(' '))

#format python's weird unicode output (probably a better way to do this, I'm not sure)
song = (song.strip('[]')[1:]).strip("''")
saveSong = song

#build the lyrics.txt file path
saveFileName = saveFileName + saveArtist + ' - ' + saveSong + ' - Lyrics.txt'

#format the artist for the genius.com url (replace spaces with '-'s) 
#and remove anything between ()'s i.e. guest features or x-editions
if song.find('(') > 0:
	song = song[:song.find('(')].strip()
song = '-'.join(song.split(' '))

#build genius.com url string
site= 'http://genius.com/' + artist + '-' + song + '-lyrics'

#thank you google - without this we recieve 403 forbidden error
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

#request page and get the div containing lyrics
#all tags within this div, that contain text, are lyrics
req = urllib2.Request(site, headers=hdr)
page = urllib2.urlopen(req)
source_code = page.read()
soup = BeautifulSoup(source_code)
content = soup.findAll('div', attrs={'class':'lyrics'})

#build lyric string
lyric = ''
for i in content:
	txt = i.text.encode('utf-8').strip()
	lyric = lyric + txt + '\n'

#write lyrics to file
file = open(saveFileName, 'w')
file.write((lyric))
file.close

#done
print 'Success!'