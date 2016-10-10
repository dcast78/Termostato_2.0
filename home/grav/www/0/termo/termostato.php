<?
preg_match('/[0-9]/', $_SERVER["DOCUMENT_URI"], $matches);
$redis_db=$matches[0];
$comando="sudo /root/termostato/termostato.py termostato_m $redis_db";
$output=`$comando`;
echo "<pre>$output</pre>";
?>
