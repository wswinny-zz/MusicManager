DROP DATABASE IF EXISTS MusicManager;
CREATE DATABASE `MusicManager` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE MusicManager;

DROP TABLE IF EXISTS Song;
DROP TABLE IF EXISTS Playlist;
DROP TABLE IF EXISTS SongPlaylist;
DROP TABLE IF EXISTS Genere;
DROP TABLE IF EXISTS Artist;

CREATE TABLE `Song` (
  `idSong` int(11) NOT NULL AUTO_INCREMENT,
  `artist` int(11) NOT NULL,
  `genere` int(11) NOT NULL,
  `songName` varchar(64) NOT NULL,
  PRIMARY KEY (`idSong`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `Playlist` (
  `idPlaylist` int(11) NOT NULL AUTO_INCREMENT,
  `playlistName` varchar(64) NOT NULL,
  PRIMARY KEY (`idPlaylist`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `SongPlaylist` (
  `idSongPlaylist` int(11) NOT NULL AUTO_INCREMENT,
  `song` int(11) NOT NULL,
  `playlist` int(11) NOT NULL,
  PRIMARY KEY (`idSongPlaylist`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `Genere` (
  `idGenere` int(11) NOT NULL AUTO_INCREMENT,
  `genereName` varchar(64) NOT NULL,
  PRIMARY KEY (`idGenere`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `Artist` (
  `idArtist` int(11) NOT NULL AUTO_INCREMENT,
  `artistName` varchar(64) NOT NULL,
  PRIMARY KEY (`idArtist`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
