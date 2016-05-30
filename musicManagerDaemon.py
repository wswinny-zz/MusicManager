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

thePeoplesMutex = threading.Lock()

def addSong(songID):
	try:
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

def getNextMessage(socket):
	data,address = socket.recvfrom(16)
	print "recv: ", data

if __name__ == "__main__":
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind(('',42069))