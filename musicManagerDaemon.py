import socket
import thread
import threading
import time
import MySQLdb
import os
import sys
import pygame
import pygame.display

#set graphics driver to dummy for headless display
#WARNING: This line makes it so you have to run the script with sudo
os.environ["SDL_VIDEODRIVER"] = "dummy"

#init pygame
pygame.init()
pygame.mixer.init()

pygame.display.init()
screen = pygame.display.set_mode((1,1))

#connect to database and setup cursor for queries
db = MySQLdb.connect(host="localhost", user="root", passwd="XDR%xdr5CFT^cft6", db="MusicManager")
cur = db.cursor()

#where the music is stored
musicDirectory = "/home/pi/Music/"
SONGEND = pygame.USEREVENT + 1

songQueue = list()		#Holds song but in what form name, id?
playSet	  = set([1,2,3,4,5,6,7,8,9])		#Holds elements of songQueue to be played

shuffle   = False		#true - on, false - off
repeat    = False		#true - on, false - off

thePeoplesMutex = threading.Lock()

def execQuery(query):
	cur.execute(query)
	return cur.fetchall()

def addSong(songID):
	try:
		songQueue.append(songID)
		thePeoplesMutex.acquire()
		playSet.add(songQueue.index(songID))

	finally:
		thePeoplesMutex.release()

def addPlaylist(playlistID):
	for row in execQuery("SELECT song FROM SongPlaylist WHERE playlist = \'" + str(playlistID) + "\'"):
		try:
			songQueue.append(row[0])
			thePeoplesMutex.acquire()
			playSet.add(songQueue.index(row[0]))
			
		finally:
			thePeoplesMutex.release()

def clear():
	try:
		songQueue = list()
		thePeoplesMutex.acquire()
		playSet.clear

	finally:
		thePeoplesMutex.release()

def skip(direction):
	return

def shuffle():
	shuffle = not shuffle

def repeat():
	repeat = not repeat

def pause():
	return

def resume():
	return

def playsong(songID):
	result = execQuery("SELECT artistName, songName FROM Song LEFT JOIN Artist ON Song.artist = Artist.idArtist WHERE idSong = " + str(songID) + ";")
	artist = result[0][0]
	song = result[0][1]

	songpath = musicDirectory + artist + "/" + song

	#plays the song 1 time using the pygame audio lib
	pygame.mixer.music.load(songpath)
	pygame.mixer.music.play(0)
	pygame.mixer.music.set_endevent(SONGEND) #fires event when the song has stopped playing

def runSongThread():
	playsong(2)

	while True:

		#pull for events using pygame
		for event in pygame.event.get():
			if event.type == SONGEND:
				print "Music Stoped playing"

		time.sleep(0.5)

if __name__ == "__main__":
	runSongThread()
	db.close()
