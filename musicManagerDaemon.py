import socket
import thread
import time
import MySQLdb

#connect to database and setup cursor for queries
db = MySQLdb.connect(host="localhost", user="root", passwd="XDR%xdr5CFT^cft6", db="MusicManager")
cur = db.cursor()

songQueue = list();									#Holds song but in what form name, id?
playSet	  = set();									#Holds elements of songQueue to be played

#Main waits for messages from PHP on port 42069
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('',42069))
while True:
    data,address = s.recvfrom(16)
    print "recv: ", data
    time.sleep(1);

def addSong(songID):
	return

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
	return