---
title: 'Gestione manuale'
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
				//sistema il cursore del range in corrispondenza della temperatura selezionata
                $('#myTable > tbody:last-child').append('<tr><td nowrap>' +  campi[1][x].replace("s_forceon","Accensione manuale").replace("s_forceoff","Spegni impianto") + '</td><td id="l_o_temp' + x + '" style="text-align:center;">' + campi[1][x] + '</td><td><center><input type=range min="1" style="width: 500px;" max="240" step="1" value=1 name="temp' + x + '" id="temp' + x + '" onclick=showVal(this.value,this.name,"temp")  /></center></td><td><output for="temp' + x + '" id="o_temp' + x + '" style="text-align:center;"></output></td></tr>');
			}
			var day=window.location.search.substr(-1);
		}

	};
	//Richiamo la pagina programmazione.php passando il querystring ricevuto che contiene ?day=1
	xhttp.open("GET", "termo/get_man.php", true);
	xhttp.send();
}
{/assets}

{assets:inline_js}
function showVal(newVal,id_elem) {
	if (id_elem.substr(0,4)=="temp") {
		document.getElementById("o_" + id_elem).value=document.getElementById(id_elem).value;
        alert("Impostata gestione manuale per " + document.getElementById(id_elem).value + "minuti!");
	}
    if (id_elem=="automatico") {
		alert("Ripristinato controllo automatico"); 
        document.getElementById("o_temp0").value=0;
        document.getElementById("o_temp1").value=0;
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
		xhttp.open("GET", "termo/salva_man.php?minuti="+newVal+"&var=" + document.getElementById("l_o_"+id_elem).innerHTML, true);
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

Puoi pilotare manualmente l'impianto forzando accensione o spegnimento per un periodo di tempo definito indipendentemente dalla temperatura impostata.

Se apri le finestre o stai uscendo puoi forzare lo spegnimento, allo stesso modo puoi forzare l'accensione manualmente su questa pagina.

I tempi sono espressi in minuti:

<table id=myTable style="table-layout: auto;">
<tbody><tr><td colspan=4 id=intestazione style="text-align:center">Impostazione manuale/automatica.</td></tr>
<tr><td colspan=4 align=center><input id=automatico type=button value="Annulla impostazione manuale" onclick="showVal('0','automatico')"></td></tr>
</tbody>
</table>
