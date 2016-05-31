<?php
	$sock = socket_create(AF_INET, SOCK_DGRAM, SOL_UDP);

	$message = $_GET['message'];
	$length = strlen($message);

	socket_sendto($sock, $message, $length, 0, '127.0.0.1', 42069);
	socket_close($sock);

	exit();

?>