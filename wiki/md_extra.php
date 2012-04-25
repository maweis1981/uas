<?php

	// $my_text = '#H1 Title#';
	$file_name = 'apis_index.md';
	$fh = fopen($file_name, "rb");
	$data = fread($fh, filesize($file_name));
	fclose($fh);
	
	include_once "markdown.php";
	$my_html = Markdown($data);
	echo $my_html;
	

?>