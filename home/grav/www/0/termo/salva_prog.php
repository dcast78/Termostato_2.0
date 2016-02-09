<?
$redis = new Redis();
//$redis->connect('127.0.0.1', 6379);
$redis_host='termostato_m';
preg_match('/[0-9]/', $_SERVER["DOCUMENT_URI"], $matches);
$redis_db=$matches[0];
$redis->connect($redis_host, 6379);
$redis->auth("Termostato_2.0");

$redis->select($redis_db);
$redis->setOption(Redis::OPT_SERIALIZER, Redis::SERIALIZER_NONE);

$giorni=array("vuoto","lun","mar","mer","gio","ven","sab","dom");
$temperature=$redis->lRange("temperature", 0, -1);
//print $_REQUEST["temp"];
$req_temp=$_REQUEST["temp"];
$req_camera=$_REQUEST["camera"];
if (is_numeric($req_temp)) {
//	print_r($temperature);
//	print_r($giorni);
	$temperatura=$temperature[$_REQUEST["temp"]];
	$programmazione=$redis->lSet($giorni[$_REQUEST["day"]], $_REQUEST["ind"],$temperatura);
	echo "day=" . $giorni[$_REQUEST["day"]] . ", index=" .  $_REQUEST["ind"] . ", temperatura=". $temperatura   ;
}
if (is_numeric($req_camera)) {
	$camere=$redis->lRange("camere", 0, -1);
	$camera=$camere[$_REQUEST["camera"]];
	$programmazione=$redis->lSet("c_" . $giorni[$_REQUEST["day"]], $_REQUEST["ind"],$camera);
	echo "c_day=c_" . $giorni[$_REQUEST["day"]] . ", camera=" . $camera;
}
?>
