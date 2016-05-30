<!DOCTYPE html>
<html>
	<?php include 'database.php'; ?>

	<head>
		<title>Playlists</title>

		<?php include 'bootstrap.php'; ?>

		<link rel='stylesheet' type='text/css' href='css/treelist.css'>
		<link rel='stylesheet' type='text/css' href='css/playlist.css'>

		<script src='js/treelist.js'></script>
	</head>
	<body>
		<form id='playlistForm' class='form-horizontal' action="postPlaylist.php" method="post">
			<div class='form-group'>
				<label class='col-sm-4 control-label'>Playlist Name</label>
				<div class='col-sm-8'>
					<input type='text' class='form-control' id='playlistName' name='playlistName' placeholder='Playlist Name' required>
				</div>
			</div>
			<div class='tree well'>
				<ul>
					<li>
						<span><i class='glyphicon glyphicon-music'></i> Music</span>
						<ul>

						<?php
							$result = mysqli_query($con, "SELECT idSong, songName, artistName FROM Song LEFT JOIN Artist ON Song.artist = Artist.idArtist ORDER BY artistName;");
							$artist = '';

							while ($row = mysqli_fetch_array($result, MYSQL_ASSOC))
							{
								if($artist != $row['artistName'] && $artist != '')
									echo "</ul></li>";

								if($artist != $row['artistName'])
									echo "<li><span><i class='glyphicon glyphicon-user'></i>" . $row['artistName'] . "</span><ul>";

								$artist = $row['artistName'];

								echo "<li><span><div id='playlistCheckbox' class='checkbox'><label><input type='checkbox' name='songs[]' value='" . $row['idSong'] . "'>" . $row['songName'] . "</label></div></span></li>";
							}

							if($artist != '')
								echo "</ul></li>";

						?>

						</ul>
					</li>
				</ul>
			</div>
			<div class="form-group">
				<div class="col-sm-offset-4 col-sm-8">
					<button type="submit" class="btn btn-default">Add Playlist</button>
				</div>
			</div>
		</form>
	</body>
</html>