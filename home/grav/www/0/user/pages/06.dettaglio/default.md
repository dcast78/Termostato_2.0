---
title: Dettaglio
---

{assets:inline_css}
.temp {
height: 30px;
width: 800px;
}
{/assets}

{assets:inline_js}

function load_data() {
	//fa una richiesta ajax per caricare la progrmmazione giornaliera e popolare la pagina
	var xhttp;
	var id_elem='';
	xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (xhttp.readyState == 4 && xhttp.status == 200) {
        	$( "#dettaglio" ).html(xhttp.responseText);
		}

	};
	//Richiamo la pagina programmazione.php passando il querystring ricevuto che contiene ?day=1
	xhttp.open("GET", "termo/termostato.php", true);
	xhttp.send();
}
{/assets}
{assets:inline_js}
//aggiunge righe e celle sulla pagina quando la pagina ha finito il primo caricamento
jQuery(document).ready( function() 
		{
		load_data();
		});
{/assets}

<div id=dettaglio>Dettaglio programmazione:</div>
