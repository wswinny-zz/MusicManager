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
suffle    = False		#true - on, false - off
repeat    = True		#true - on, false - off

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

def runSongThread():
	return

if __name__ == "__main__":
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind(('',42069))

	data,address = socket.recvfrom(16)
	print "recv: ", data

	db.close()