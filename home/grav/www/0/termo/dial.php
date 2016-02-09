<!doctype html>
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
$camere=$redis->lRange("camere", 0, -1);
for ($x=0;$x<count($camere);$x++) {
 $temp=$redis->lRange($camere[$x], -1, -1);
 $s_temp.=$temp[0] . "," ;
}
$s_temp=substr($s_temp, 0, -1);
?>
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
    <title>dials</title>       
    
    <script type="text/javascript" src="http://mbostock.github.com/d3/d3.min.js"></script>
    <script type="text/javascript" src="dial_chart.php"></script>

    <style type="text/css">

    #dial-0 .needle path {
      fill: #b21f24;
    }

    #dial-1 .needle path {
      fill: #b21f24;
    }

    #dial-2 .needle path {
      fill: #b21f24;
    }

    circle.label {
      fill: white;
    }       
    
    line.label {
      stroke: white; 
      stroke-width: 1px;
    }
    
    text.label {
      font-family: Arial;
      font-size: 12px;
      fill: white; 
    }

    #dial-0 text.label {
      font-size: 16px;      
    } 
    #dial-1 text.label {
      font-size: 16px;      
    } 
    #dial-2 text.label {
      font-size: 16px;      
    } 

    </style>

  </head>
<body style="background-color:#7D8B9C">
  <div id="chart">
  </div>
  <script type="text/javascript">

    (function(chartselector) {
      var temperatura = [<?=$s_temp?>];
      var w = 1900,
          h = 800;

      var layout = [ 
        { x: 200, y: 250, r: 200, m: 14, M: 30, ticks: 4, mark: 'circle', temp: 25}, 
        { x: 650, y: 250, r: 200, m: 14, M: 30, ticks: 4, mark: 'circle', temp: 18}, 
        { x: 1100, y: 250, r: 200, m:14, M: 30, ticks: 4, mark: 'circle', temp:21 } 
      ];
      var charts = layout.map(function(d) { 
        return NBXDialChart()
          .width(d.r * 2)
          .height(d.r * 2)
          .domain([d.m, d.M])
          .range([-150, 150])
          .minorTicks(d.ticks)
          .minorMark(d.mark);
      });      
      
      var svg = d3.select(chartselector)
        .append('svg:svg')
          .attr('width', w) 
          .attr('height', h);
      
      var dials = svg.selectAll('g.dial')
          .data(layout)
        .enter().append('svg:g')
          .attr('class', 'dial')
          .attr('id', function(d, i) { return 'dial-' + i; })
          .attr('transform', function(d) { return 'translate(' + (d.x - d.r) + ',' + (d.y - d.r) + ')'; } );

      dials.each(function(d, i) { d3.select(this).data([20]).call(charts[i]); });

      window.transition = function() {
        dials.each(function(d, i) { 
          d3.select(this)
	    .data([ temperatura[i] ])
            .call(charts[i]); 
        });
      };

    })('#chart');

transition();
  </script>
</body>
</html>

