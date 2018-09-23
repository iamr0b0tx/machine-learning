<?php

if(isset($_REQUEST["get_position"])){
	$file = $_REQUEST["get_position"];
	
	$f = fopen($file, "r");
	$r = fgets($f);
	fclose($f);
	
	echo $r;

}elseif(isset($_REQUEST["set_position"])){
	$val = $_REQUEST["set_position"];
	
	$f = fopen("target.json", "w");
	$r = fwrite($f, $val);
	fclose($f);
	
	echo $r;

}

?>