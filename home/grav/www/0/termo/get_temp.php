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
$programmazione[1]=$redis->lRange("temperature", 0, -1);
for ($temperatura=0 ; $temperatura<count($programmazione[1]) ; $temperatura++) {
 $t_min=$redis->get($programmazione[1][$temperatura] . "_min");
 $t_max=$redis->get($programmazione[1][$temperatura] . "_max");
 $programmazione[1]=$redis->lRange("temperature", 0, -1);
 $programmazione[0][$temperatura]=($t_min+$t_max)/2;
}
echo json_encode ($programmazione);
?>
