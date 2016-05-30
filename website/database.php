<?php
	$servername = 'localhost';
	$username 	= 'root';
	$password 	= 'XDR%xdr5CFT^cft6';
	$database 	= 'MusicManager';

	$con = mysqli_connect($servername, $username, $password, $database);

	if (mysqli_connect_errno())
	    echo "Connection failed: " . mysqli_connect_error();
?>