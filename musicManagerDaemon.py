import socket
import thread
import threading
import time
import MySQLdb

#connect to database and setup cursor for queries
db = MySQLdb.connect(host="localhost", user="root", passwd="XDR%xdr5CFT^cft6", db="MusicManager")
cur = db.cursor()

songQueue = list()		#Holds song but in what form name, id?
playSet	  = set()		#Holds elements of songQueue to be played
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
	for row in execQuery("SELECT song FROM SongPlaylist WHERE playlist = '" + playlistID + "'")
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
	shuffle = !shuffle

def repeat():
	repeat = !repeat

def pause():
	

def resume():
	return

def runSongThread():
	return

if __name__ == "__main__":
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind(('',42069))

	data,address = socket.recvfrom(16)
	print "recv: ", data

	db.close()