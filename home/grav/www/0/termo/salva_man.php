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
if ($_REQUEST["var"]=="s_forceon") {
$redis->delete("s_forceoff");
$redis->set($_REQUEST["var"], 1);
$redis->expire($_REQUEST["var"] , $_REQUEST["minuti"] * 60 );
$redis->publish("rele_ch",1);
$redis->lset("rele",-1,1);
} 
if ($_REQUEST["var"]=="s_forceoff") {
$redis->delete("s_forceon");
$redis->set($_REQUEST["var"], 1);
$redis->expire($_REQUEST["var"] , $_REQUEST["minuti"] * 60 );
$redis->publish("rele_ch",0);
$redis->lset("rele",-1,0);
} 
if ($_REQUEST["var"]=="automatico") {
$redis->delete("s_forceoff");
$redis->delete("s_forceon");
}
?>
