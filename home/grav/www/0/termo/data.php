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
$sensori= $redis->lRange("camere", 0, -1);
if ($_REQUEST["start"]) {
 $start=$_REQUEST["start"];
} else {
 $start=-576;
}
if ($_REQUEST["stop"]) {
 $stop=$_REQUEST["stop"];
} else {
 $stop=-1;
}
for ($j=0; $j<count($sensori); $j++) {
	$letture[$j]= $redis->lRange($sensori[$j], $start, $stop);
}
$intestazione="date\t";
for ($x=0; $x<count($sensori); $x++) {
	$intestazione.=$sensori[$x]."\t";
}
$intestazione=substr($intestazione,0,-1);
$intestazione.="\r\n";
print $intestazione;
$timestamp= $redis->lRange("timestamp", $start, $stop);
for ($x=0 ; $x<count($letture[0]); $x++) {
	$riga=date('YmdHis',$timestamp[$x]);
	for ($j=0; $j<count($sensori); $j++) {
		if ($sensori[$j]=="rele") {
			$riga.="\t"; 
			$riga.=$letture[$j][$x]+18;
		} else {
			$riga.="\t" . floatval($letture[$j][$x]);
		}
	}
	$riga.="\r\n";
	print $riga;
}?>
