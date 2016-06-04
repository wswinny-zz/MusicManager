<!DOCTYPE html>
<html>
	<?php include 'bootstrap.php'; ?>
	<head>
		<title>Music Manager System</title>
		<?php include 'bootstrap.php'; ?>

		<link rel='stylesheet' type='text/css' href='css/uploadSong.css'>

		<script src='js/uploadSong.js'></script>
	</head>
	<body>
		<form id="uploadSongForm" class="form-horizontal" action="postUploadSong.php" method="post" enctype="multipart/form-data">
			<div class="form-group">
				<div class="col-sm-12">

					<div class="input-group">
						<label class="input-group-btn">
							<span class="btn btn-primary">
								Browse Songs <input type="file" name="files[]" id="fileToUpload" style="display: none;" multiple>
							</span>
						</label>
						<input type="text" class="form-control" readonly>
					</div>
				</div>
			</div>

			<div class='form-group'>
				<div class='col-sm-12'>
					<input type='text' class='form-control' name='artist' placeholder='Song Artist' required>
				</div>
			</div>

			<div class='form-group'>
				<div class='col-sm-12'>
					<input type='text' class='form-control' name='genre' placeholder='Song Genre' required>
				</div>
			</div>

			<div class="form-group">
				<div class="col-sm-12">
					<button type="submit" class="btn btn-default">Upload Song(s)</button>
				</div>
			</div>
		</form>
	</body>
</html>