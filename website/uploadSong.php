<!DOCTYPE html>
<html>
	<?php include 'bootstrap.php'; ?>
	<body>

		<form action="postUploadSong.php" method="post" enctype="multipart/form-data">
		    Select song to upload:
		    <input type="file" name="fileToUpload" id="fileToUpload"><br>
		    Artist:
		    <input type="text" name="artist" id="artist"><br>
		    Genre:
		    <input type="text" name="genre" id="genre"><br>
		    <input type="submit" value="Upload Song" name="submit">
		</form>

	</body>
</html>