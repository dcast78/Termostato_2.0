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
$giorno=$_REQUEST["day"];
$giorni=array("vuoto","lun","mar","mer","gio","ven","sab","dom");
$camere=$redis->lRange("camere", 0, -1);
$key = array_search('rele',$camere);
if($key!==false){
    unset($camere[$key]);
}
$key = array_search('setpoint',$camere);
if($key!==false){
    unset($camere[$key]);
}

for ($x=0;$x<=count($camere)+1;$x++) {
 if ($camere[$x]) {
  $programmazione[0][]=$camere[$x];
 }
}
$programmazione[1]=$redis->lRange("temperature", 0, -1);


$prog_giorno= $redis->lRange($giorni[$giorno], -48, -1);
$prog_camera= $redis->lRange("c_" . $giorni[$giorno], -48, -1);
for ($ora=0 ; $ora<=47 ; $ora++) {
 $programmazione[2][$ora]=$prog_giorno[$ora];
 $programmazione[3][$ora]=$prog_camera[$ora];
}
$programmazione[4]=array("vuoto","lun","mar","mer","gio","ven","sab","dom");
echo json_encode ($programmazione);
?>
