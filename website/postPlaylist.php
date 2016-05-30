<!DOCTYPE HTML>
<html>
	<head>
	</head>
	<body>
		<?php

			error_reporting(E_ALL);
			ini_set('display_errors', 1);

			include("database.php");
			
			$playlistName = $_POST['playlistName'];
			$songs = $_POST['songs'];

			$result = mysqli_query($con, "SELECT playlistName FROM Playlist;");
			while ($row = mysqli_fetch_array($result, MYSQL_ASSOC))
			{
				if($playlistName == $row['playlistName'])
					die();
			}

			mysqli_query($con, "INSERT INTO Playlist (playlistName) VALUES ('$playlistName');");
			
			$result = mysqli_query($con, "SELECT idPlaylist FROM Playlist ORDER BY idPlaylist DESC LIMIT 1;");
			$row = mysqli_fetch_array($result, MYSQL_ASSOC);

			$playlistid = $row['idPlaylist'];

			for($i = 0; $i < count($songs); $i++)
			{	
				$songid = $songs[$i];
				$result = mysqli_query($con, "INSERT INTO SongPlaylist (song, playlist) VALUES ('$songid', '$playlistid');");
			}

			header('Location: playlist.php');
			exit;

			mysql_close($con);

		?>
	</body>
</html>