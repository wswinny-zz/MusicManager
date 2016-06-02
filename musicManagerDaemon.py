#!/usr/bin/python
import socket
import threading
import time
import MySQLdb
import os
import sys
import pygame
import random
import signal

from threading import Thread

def execQuery(query):
	cur.execute(query)
	return cur.fetchall()

#adds song to sognQueue by its id and updates the playSet
def addSong(songID):
	try:
		thePeoplesMutex.acquire()
		songQueue.append(songID)

		if len(songQueue) - 1 == len(songHistory) and currentlyPlaying == -1:
			playNextSong()

	finally:
		thePeoplesMutex.release()

#adds all songs in a playlist to the songQueue by their ids and updates the playSet
def addPlaylist(playlistID):
	for row in execQuery("SELECT song FROM SongPlaylist WHERE playlist = " + str(playlistID) + ";"):
		addSong(row[0])

#adds all songs in a Artist to the songQueue by their ids and updates the playSet
def playAllArtist(ArtistID):
	for row in execQuery("SELECT idSong FROM Song WHERE artist = " + str(ArtistID) + ";"):
		addSong(row[0])

#adds all songs in a Genre to the songQueue by their ids and updates the playSet
def playAllGenre(genreID):
	for row in execQuery("SELECT idSong FROM Song WHERE genere = " + str(genreID) + ";"):
		addSong(row[0])

#clears the queue
def clear():
	global songQueue
	global songHistory
	global songPtr

	try:
		thePeoplesMutex.acquire()
		songQueue = list()
		songHistory = list()
		songPtr = 0

	finally:
		thePeoplesMutex.release()

def shufflePlaylist():
	global shuffle
	shuffle = not shuffle

def repeatPlaylist():
	global repeat
	repeat = not repeat

def pause():
	pygame.mixer.music.pause()

def resume():
	pygame.mixer.music.unpause()

def repopulate():
	global songHistory
	global songPtr

	songHistory = list()
	songPtr = 0

def playNextSong(direction = 1):
	global currentlyPlaying
	global songHistory

	if currentlyPlaying != -1 and direction == 1:
		songHistory.append(currentlyPlaying) #adds the song to the history list
		print "Either Thread: Appending the song ", currentlyPlaying, " to the song history"

	currentlyPlaying = -1

	availableQueue = list(set(songQueue) - set(songHistory))
	availableQueueLength = len(availableQueue)

	if (availableQueueLength == 0 and direction == 1) or len(songQueue) == 0:
		if repeat:
			repopulate()
			availableQueue = list(set(songQueue) - set(songHistory))
			availableQueueLength = len(availableQueue)
		else:
			return

	if direction == 1:
		if shuffle:
			randomSong = int(random.randRange(0, availableQueueLength)) % availableQueueLength
			playSong(availableQueue[randomSong])
		if not shuffle:
			playSong(next(iter(availableQueue)))
	else:
		if len(songHistory) > 0:
			lastSongPlayed = songHistory.pop()
			playSong(lastSongPlayed)

def playSong(songID):
	global songPtr
	global currentlyPlaying

	result = execQuery("SELECT artistName, songName FROM Song LEFT JOIN Artist ON Song.artist = Artist.idArtist WHERE idSong = " + str(songID) + ";")
	artist = result[0][0]
	song = result[0][1]

	songpath = musicDirectory + artist + "/" + song

	print "Thread 1: Playing song ", song, " by artist ", artist

	#plays the song 1 time using the pygame audio lib
	pygame.mixer.music.load(songpath)
	pygame.mixer.music.play(0)

	songPtr = songQueue.index(songID)
	currentlyPlaying = songID

def runSongThread():
	while running:
		#pull to check if the mixer is no longer playing a song if so try to play somthing
		if not pygame.mixer.music.get_busy():
			playNextSong()
			print "Thread 1: Player not busy playing next song"

		time.sleep(0.5)

def sighandler(signal, frame):
	global running

	print("Main Thread: Signal caught exiting gracefully")
	running = False
	sys.exit(0)

#init pygame
pygame.init()
pygame.mixer.init()

print "Main Thread: PyGame init complete"

#connect to database and setup cursor for queries
db = MySQLdb.connect(host="localhost", user="root", passwd="XDR%xdr5CFT^cft6", db="MusicManager")
cur = db.cursor()

print "Main Thread: Database connected"

#where the music is stored
musicDirectory = "/home/pi/Music/"

songQueue = list() #Holds song but in what form name, id?
songHistory = list() #Holds the play history of the queue
songPtr = 0 #holds the currently selected song
currentlyPlaying = -1 	#holds the currently playing song
						#if this is -1 that means nothing is playing

shuffle   = False							#true - on, false - off
repeat    = False							#true - on, false - off

thePeoplesMutex = threading.Lock()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

running = True
thread = Thread(target = runSongThread)

print "Main Thread: Created all local varibles"

if __name__ == "__main__":

	#Init signal handler
	print "Main Thread: Trapping all signals"

	signal.signal(signal.SIGINT, 	sighandler)
	signal.signal(signal.SIGHUP, 	sighandler)
	signal.signal(signal.SIGTERM, 	sighandler)
	signal.signal(signal.SIGTSTP, 	sighandler)
	signal.signal(signal.SIGQUIT, 	sighandler)

	print "Main Thread: Signals handled"

	try:
		thread.start()

		print "Main Thread: Created Thread 1"
	except:
		print "Error: unable to start thread"

	
	s.bind(('',42069))

	while True:
		print "Main Thread: Waiting for data"
		
		data,address = s.recvfrom(16)
		
		print "Main Thread: Got: ", data, " from ", address

		data = data.split("-")

		if data[0] == 's':
			addSong(int(data[1]))
		if data[0] == 'p':
			pause()
		if data[0] == 'sf':
			playNextSong(1)
		if data[0] == 'sb':
			playNextSong(-1)
		if data[0] == 'shuf':
			shufflePlaylist()
		if data[0] == 'c':
			clear()
		if data[0] == 'rep':
			repeatPlaylist()
		if data[0] == 'r':
			resume()
		if data[0] == 'pa':
			playAllArtist(int(data[1]))
		if data[0] == 'pg':
			playAllGenre(int(data[1]))

		print "Main Thread: After checking if statements"

	db.close()
