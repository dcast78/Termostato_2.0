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

$redis->delete("s_forceon");
$redis->set("s_forceoff",1)
$redis->expire("s_forceoff",1800)
$redis->publish("rele_ch",0)
$redis->rpush("rele",0)

$redis->delete("s_forceoff"e
$redis->set("s_forceon",1)
$redis->expire("s_forceon",1800)
$redis->publish("rele_ch",1)
$redis->rpush("rele",1)

$redis->delete("s_forceon"e
$redis->delete("s_forceoff")
cmd='sudo /root/termostato/termostato.py ' + db_host + ' ' + db_id
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    out = proc.stdout.read()
    bot.sendMessage(update.message.chat_id, text=out)

