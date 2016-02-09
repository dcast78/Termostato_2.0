---
title: 'Programma orario'
---

{assets:inline_css}
.temp {
height: 30px;
width: 800px;
}
{/assets}

{assets:inline_js}

function load_data() {
	//fa una richiesta ajax per caricare la programmazione giornaliera e popolare la pagina
	var xhttp;
	var id_elem='';
	xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (xhttp.readyState == 4 && xhttp.status == 200) {
			campi=JSON.parse(xhttp.responseText);
			for (x=0;x<=47;x++) {
				//aggiusta il numero di step dell'input range in base al numero al numero di temperature impostabili e lette dal db redis
				document.getElementById("temp" + x).max=campi[1].length-1;
				//sistema il cursore del range in corrispondeza della temperatura selezionata
				document.getElementById("temp" + x).value=campi[1].indexOf(campi[2][x]);
				document.getElementById("o_temp" + x).value=campi[2][x];
				//aggiusta il numero di step dell'input range in base al numero al numero di camere configurabili e lette dal db redis
				document.getElementById("camera" + x).max=campi[0].length-1;
				document.getElementById("camera" + x).value=campi[0].indexOf(campi[3][x]);
				document.getElementById("o_camera" + x).value=campi[3][x];
			}
			var day=window.location.search.substr(-1);
			document.getElementById("intestazione").innerHTML+="<b>Programmazione giornaliera "+campi[4][day]+"</b>";
		}

	};
	//Richiamo la pagina programmazione.php passando il querystring ricevuto che contiene ?day=1
	xhttp.open("GET", "termo/programmazione.php" + window.location.search, true);
	xhttp.send();
}
{/assets}

{assets:inline_js}
function showVal(newVal,id_elem) {
	if (id_elem.substr(0,4)=="temp") {
		document.getElementById("o_" + id_elem).value=campi[1][newVal];  
        console.log(document.getElementById("o_" + id_elem).value);
	}
	if (id_elem.substr(0,6)=="camera") {
		document.getElementById("o_" + id_elem).value=campi[0][newVal];
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
		xhttp.open("GET", "termo/salva_prog.php" +  window.location.search + "&" +elem_type[0]+"="+newVal+"&ind="+prog[0], true);
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
		for (x=0; x<=47; x++) {
		if (x%2==0) {min="00"} else {min="30"}; 
		$('#myTable > tbody:last-child').append('<tr><td>'+Math.floor(x/2)+':'+min+'</td><td><input type=range min="0" max="3" id="temp' + x + '" name="temp' + x + '" onclick=showVal(this.value,this.name,"temp")  /></td><td><output for="temp' + x + '" id="o_temp' + x + '"></output></td><td>Camera</td><td><input type=range min="0" max="3" id="camera' + x + '" name="camera' + x + '" onclick=showVal(this.value,this.name,"camera")  /></td><td><output for="camera' + x + '" id="o_camera' + x + '"></output></td></tr>');
		} 
		load_data();
		});
{/assets}

<table id=myTable style="table-layout: auto;">
<tbody><tr><td colspan=6 id=intestazione style="text-align:center"></td></tr>
</tbody>
</table>
