<!DOCTYPE html>
<html>
	<?php include 'database.php'; ?>

	<head>
		<title>Music Manager System</title>
		<?php include 'bootstrap.php'; ?>

		<link rel='stylesheet' type='text/css' href='css/index.css'>
		<link rel='stylesheet' type='text/css' href='css/treelist.css'>

		<script src='js/index.js'></script>
		<script src='js/treelist.js'></script>
	</head>
	<body>
		<form id='mainForm' class="form-horizontal">
			<div id="tree" class="form-group">
				<div class="col-sm-12">
					<div class='tree'>
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

									echo "<li><span><i class='glyphicon glyphicon-plus addSongButton' songid='" . $row['idSong'] . "'></i>" . $row['songName'] . "</span></li>";
								}

								if($artist != '')
									echo "</ul></li>";
							?>
						</ul>
					</div>
				</div>
			</div>
			<div id="controls" class="form-group">
				<div class="col-sm-12">
					<div class='controls'>
						<p class="glyphicon glyphicon-repeat control repeat" aria-hidden="true"></p>
						<p class="glyphicon glyphicon-play control play" aria-hidden="true"></p>
						<p class="glyphicon glyphicon-random control shuffle" aria-hidden="true"></p>
					</div>
					<div class='controls'>
						<p class="glyphicon glyphicon-backward control backward" aria-hidden="true"></p>
						<p class="glyphicon glyphicon-pause control pause" aria-hidden="true"></p>
						<p class="glyphicon glyphicon-forward control forward" aria-hidden="true"></p>
					</div>
				</div>
			</div>
		</form>

		<script type="text/javascript">
			$( ".addSongButton" ).click(function() {
				sendMessageOverSocket('s-' + $( this ).attr('songid'));
			});

			$( ".play" ).click(function() {
				sendMessageOverSocket('r');
			});

			$( ".backward" ).click(function() {
				sendMessageOverSocket('sb');
			});

			$( ".pause" ).click(function() {
				sendMessageOverSocket('p');
			});

			$( ".forward" ).click(function() {
				sendMessageOverSocket('sf');
			});

			$( ".shuffle" ).click(function() {
				sendMessageOverSocket('shuf');
			});

			$( ".repeat" ).click(function() {
				sendMessageOverSocket('rep');
			});
		</script>
	</body>
</html>