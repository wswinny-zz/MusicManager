import socket
import thread
import threading
import time
import MySQLdb
import os
import sys
import pygame

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

songQueue = list() #Holds song but in what form name, id?
songHistory = list() #Holds the play history of the queue
playSet	= set([1,2,3,4,5,6,7,8,9]) #Holds elements of songQueue to be played

shuffle   = False							#true - on, false - off
repeat    = False							#true - on, false - off

thePeoplesMutex = threading.Lock()

def execQuery(query):
	cur.execute(query)
	return cur.fetchall()

#adds song to sognQueue by its id and updates the playSet
def addSong(songID):
	try:
		thePeoplesMutex.acquire()
		songQueue.append(songID)

	finally:
		thePeoplesMutex.release()

#adds all songs in a playlist to the songQueue by their ids and updates the playSet
def addPlaylist(playlistID):
	for row in execQuery("SELECT song FROM SongPlaylist WHERE playlist = " + str(playlistID) + ";"):
		try:
			thePeoplesMutex.acquire()
			songQueue.append(row[0])
			
		finally:
			thePeoplesMutex.release()

#clears the queue
def clear():
	try:
		thePeoplesMutex.acquire()
		songQueue = list()
		songHistory = list()
		songPtr = 0

	finally:
		thePeoplesMutex.release()

def shuffle():
	shuffle = not shuffle

def repeat():
	repeat = not repeat

def pause():
	pygame.mixer.music.pause()

def resume():
	pygame.mixer.music.unpause()

def repopulate():
	songHistory = list()
	songPtr = 0

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
				if len(playSet) == 0 && repeat:
					repopulate()
				if len(playSet) > 0 && shuffle:
					playsong(playSet.pop())
				if len(playSet) > 0 && not shuffle:
					nextSong = next(iter(playSet))

					playsong(nextSong)
					playSet.remove(nextSong)

		time.sleep(0.5)

if __name__ == "__main__":
	runSongThread()
	db.close()
