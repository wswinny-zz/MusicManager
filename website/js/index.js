function sendMessageOverSocket(message)
{
	console.log("clicked");

	$.ajax({
		type: "GET",
		url: "sendMessage.php?message=" + message, 
		cache: false,

		success: function (data)
		{
			console.log('SUCUESS');
		},
		
		error: function (XMLHttpRequest, textStatus, errorThrown) 
		{
			console.log('FAILURE');
		},
		
		async: false
	});
}