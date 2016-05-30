<?php
	include 'database.php';

	//Users must come from uploadSong.php
	if(!isset($_POST["submit"]))
	{
		echo "GTFO";
		exit();
	}

	$fileTypes    = array("mp3");								//Accepted file types to be uploaded
	$target_dir   = "/home/pi/Music/";							//Folder all music will be placed in
	$uploadOk     = true;											//If all data was entered correctly
	$artistExists = true;											
	$genreExists  = true;
	$songName     = $_FILES["fileToUpload"]["name"];
	$songFileType = pathinfo(basename($_FILES["fileToUpload"]["name"]),PATHINFO_EXTENSION);

	//Checks valid file tpye
	if(!in_array($songFileType, $fileTypes))
	{
		
		echo "Your song must be one of the following filetypes:<br>";

		foreach ($fileTypes as $type) 
		{
			echo $type . "<br>";
		}
		echo "<br>";
		
		$uploadOk = false;
	}

	if(!isset($_POST["artist"]))
	{
		echo "Your song must have a artist<br>";

		$uploadOk = false;
	}

	if(!isset($_POST["genre"]))
	{
		echo "Your song must have a genre<br>";

		$uploadOk = false;
	}

	if(!$uploadOk)
		exit();

	//set complete save path for song
	$artist      = strtolower($_POST["artist"]);
	$artistPath  = $target_dir . $artist;
	$target_file = $target_dir . "$artist/" . basename($_FILES["fileToUpload"]["name"]);
	$genre       = strtolower($_POST["genre"]);

	if(!is_dir($artistPath))
	{
		mkdir($artistPath);
		$artistExists = false;
	}
	
	if(file_exists($target_file))
	{
		echo "Song already uploaded<br>";

		exit();
	}

	$query = "SELECT idGenere FROM Genere WHERE genereName = '$genre'";
	$result = mysqli_query($con, $query);

	if (mysqli_num_rows($result) == 0) 
	    $genreExists = false;

	if(!$artistExists)
	{
		$query = "INSERT INTO Artist (artistName) VALUES ('$artist')";
		$result = mysqli_query($con, $query);
	}

	if(!$genreExists)
	{
		$query = "INSERT INTO Genere (genereName) VALUES ('$genre')";
		$result = mysqli_query($con, $query);
	}

	//Fancy Query
	$query = "INSERT INTO Song (artist, genere, songName) VALUES ((SELECT idArtist FROM Artist WHERE artistName = '$artist'), (SELECT idGenere FROM Genere WHERE genereName = '$genre'), '$songName')";
	$result = mysqli_query($con, $query);
	if(!$result)
	{
		echo "Insertion Failed<br>";
		exit();
	}

	if(move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file))
		echo "File Uploaded!<br>";
	else
		echo "Upload Failed<br>";

	mysql_close($con);

	header('Location: uploadSong.php');
	exit;

?>