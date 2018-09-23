<?php

if(isset($_REQUEST["q"])){
	$file = $_REQUEST["q"];
	
	$f = fopen($file, "r");
	$r = fgets($f);
	fclose($f);
	
	echo $r;

}

?>