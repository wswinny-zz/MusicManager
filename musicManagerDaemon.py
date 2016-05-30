import socket
import thread
import threading
import time
import MySQLdb

from pygame import mixer

#connect to database and setup cursor for queries
db = MySQLdb.connect(host="localhost", user="root", passwd="XDR%xdr5CFT^cft6", db="MusicManager")
cur = db.cursor()

musicDirectory = "/home/pi/Music/"

songQueue = list()		#Holds song but in what form name, id?
playSet	  = set([1,2,3,4,5,6,7,8,9])		#Holds elements of songQueue to be played

shuffle   = False		#true - on, false - off
repeat    = False		#true - on, false - off

thePeoplesMutex = threading.Lock()

def execQuery(query):
	cur.execute(query)
	return cur.fetchall()

#adds song to sognQueue by its id and updates the playSet
def addSong(songID):
	try:
		songQueue.append(songID)
		thePeoplesMutex.acquire()
		playSet.add(songQueue.index(songID))

	finally:
		thePeoplesMutex.release()

#adds all songs in a playlist to the songQueue by their ids and updates the playSet
def addPlaylist(playlistID):
	for row in execQuery("SELECT song FROM SongPlaylist WHERE playlist = \'" + str(playlistID) + "\'"):
		try:
			songQueue.append(row[0])
			thePeoplesMutex.acquire()
			playSet.add(songQueue.index(row[0]))
			
		finally:
			thePeoplesMutex.release()

#clears the queue
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

def repopulate():
	return

def playsong(songID):
	result = execQuery("SELECT artistName, songName FROM Song LEFT JOIN Artist ON Song.artist = Artist.idArtist WHERE idSong = " + str(songID) + ";")
	artist = result[0][0]
	song = result[0][1]

	return musicDirectory + artist + "/" + song

def runSongThread():
	while True:
			

if __name__ == "__main__":
	playsong(2)
	db.close()
