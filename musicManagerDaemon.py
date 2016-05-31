import socket
import thread
import threading
import time
import MySQLdb
import os
import sys
import pygame
import random

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
songPtr = 0 #holds the currently selected song
currentlyPlaying = -1 	#holds the currently playing song
						#if this is -1 that means nothing is playing

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

		if len(sognQueue) - 1 == len(songHistory) && currentlyPlaying == -1:
			playNextSong()

	finally:
		thePeoplesMutex.release()

#adds all songs in a playlist to the songQueue by their ids and updates the playSet
def addPlaylist(playlistID):
	for row in execQuery("SELECT song FROM SongPlaylist WHERE playlist = " + str(playlistID) + ";"):
		addSong(row[0])

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

def playNextSong(direction = 1):
	availableQueue = list(set(songQueue) - set(songHistory))
	availableQueueLength = len(availableQueue)

	if currentlyPlaying != -1:
		songHistory.append(currentlyPlaying) #adds the song to the history list

	if availableQueueLength == 0:
		if repeat:
			repopulate()
		else:
			return

	if direction == 1:
		if shuffle:
			randomSong = random.random() % availableQueueLength
			playsong(availableQueue[randomSong])
		if not shuffle:
			nextSong = (availableQueue.index(songQueue[songPtr]) + 1) % availableQueueLength
			playSong(availableQueue[nextSong])
	else:
		lastSongPlayed = songHistory.pop()
		playSong(lastSongPlayed)

def playsong(songID):
	result = execQuery("SELECT artistName, songName FROM Song LEFT JOIN Artist ON Song.artist = Artist.idArtist WHERE idSong = " + str(songID) + ";")
	artist = result[0][0]
	song = result[0][1]

	songpath = musicDirectory + artist + "/" + song

	#plays the song 1 time using the pygame audio lib
	pygame.mixer.music.load(songpath)
	pygame.mixer.music.play(0)
	pygame.mixer.music.set_endevent(SONGEND) #fires event when the song has stopped playing

	songPtr = songQueue.index(songID)
	currentlyPlaying = songID

def runSongThread():
	playsong(2)

	while True:
		#pull for events using pygame
		for event in pygame.event.get():
			if event.type == SONGEND:
				playNextSong()

		time.sleep(0.5)

if __name__ == "__main__":
	runSongThread()
	db.close()
