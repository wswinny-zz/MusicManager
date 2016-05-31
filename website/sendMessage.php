<?php
	$sock = socket_create(AF_INET, SOCK_DGRAM, SOL_UDP);

	$message = $_GET['message'];
	echo $message . "<br>";
	$length = strlen($message);

	socket_sendto($sock, $message, $length, 0, '127.0.0.1', 42069);
	echo "message sent";
	socket_close($sock);

	exit();

?>