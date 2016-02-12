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
$programmazione[1][0]="s_forceon";
$programmazione[1][1]="s_forceoff";
$programmazione[0][0]=$redis->get("s_forceon");
$programmazione[0][1]=$redis->get("s_forceoff");
echo json_encode ($programmazione);
?>
