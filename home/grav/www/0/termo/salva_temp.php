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
$t_min=$_REQUEST["temp"]-0.25;
$t_max=$_REQUEST["temp"]+0.25;
$redis->set($_REQUEST["n_temp"] . "_min", $t_min);
$redis->set($_REQUEST["n_temp"] . "_max", $t_max);
?>
