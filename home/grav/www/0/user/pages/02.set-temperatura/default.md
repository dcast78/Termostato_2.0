---
title: 'Set temperatura'
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
			campi=JSON.parse(xhttp.responseText);
			console.log(campi);
			//numero di temperature impostabili e lette dal db redis
			for (x=0;x<=campi[1].length-1;x++) {
				//sistema il cursore del range in corrispondeza della temperatura selezionata
		$('#myTable > tbody:last-child').append('<tr><td id="l_o_temp' + x + '" style="text-align:center;">' + campi[1][x] + '</td><td><center><input type=range min="18" style="width: 500px;" max="24" step="0.05" value="' + campi[0][x] + '" id="temp' + x + '" name="temp' + x + '" onclick=showVal(this.value,this.name,"temp")  /></center></td><td><output for="temp' + x + '" id="o_temp' + x + '" style="text-align:center;">' + campi[0][x] + '</output></td></tr>');
				//document.getElementById("temp" + x).value=campi[1].indexOf(campi[2][x]);
				//document.getElementById("o_temp" + x).value=campi[2][x];
			}
			var day=window.location.search.substr(-1);
			document.getElementById("intestazione").innerHTML+="Imposta temperatura";
		}

	};
	//Richiamo la pagina programmazione.php passando il querystring ricevuto che contiene ?day=1
	xhttp.open("GET", "termo/get_temp.php", true);
	xhttp.send();
}
{/assets}

{assets:inline_js}
function showVal(newVal,id_elem) {
	if (id_elem.substr(0,4)=="temp") {
		document.getElementById("o_" + id_elem).value=document.getElementById(id_elem).value;   
	}
	var xhttp;
	xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (xhttp.readyState == 4 && xhttp.status == 200) {
			console.log(xhttp.responseText);

		}
	};
	elem_type=id_elem.match(/[a-z]+/) //divido il_elem es:temp0 in un array con la prima parte stringa e seconda parte numeri
		prog=id_elem.match(/[0-9]+/) //divido il_elem es:temp0 in un array con la prima parte stringa e seconda parte numeri
		//Richiamo la pagina salva.php passando il querystring ricevuto che contiene ?day=1 e aggiungendo i parametri delle var da salvare
		xhttp.open("GET", "termo/salva_temp.php?temp="+newVal+"&n_temp=" + document.getElementById("l_o_"+id_elem).innerHTML, true);
	xhttp.send();    
}

{/assets}
{assets:inline_js}
function outputUpdate(temp,id) {
	document.querySelector('#'+id+'_gradi').value = temp;
}
{/assets}
{assets:inline_js}
//aggiunge righe e celle sulla pagina quando la pagina ha finito il primo caricamento
jQuery(document).ready( function() 
		{
		load_data();
		});
{/assets}

<table id=myTable style="table-layout: auto;">
<tbody><tr><td colspan=3 id=intestazione style="text-align:center"></td></tr>
</tbody>
</table>
