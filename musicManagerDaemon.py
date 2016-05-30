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

suffle    = False		#true - on, false - off
repeat    = False		#true - on, false - off

thePeoplesMutex = threading.Lock()

def execQuery(query):
	cur.execute(query)
	return cur.fetchall()

def addSong(songID):
	try:
		songQueue.append(songID)
		
		thePeoplesMutex.acquire()
		#code goes here
	finally:
		thePeoplesMutex.release()

def addPlaylist(playlistID):
	return

def clear():
	return

def skip(direction):
	return

def shuffle(isShuffling):
	return

def repeat(doRepeat):
	return

def pause():
	return

def resume():
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
