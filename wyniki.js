url2="http://0.0.0.0:6543";
var wyniki;

function drawTrace(id){
    $.ajax({
        type: 'GET',
        url: url2+"/api/trace/".concat(id),
        data: JSON.stringify(payload),
        headers: {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST,GET,DELETE,PUT,OPTIONS',
            'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, Authorization',
            'Access-Control-Allow-Credentials': 'true'
        },
        contentType: "application/json",
        dataType: 'json',
        crossDomain: true,
        async:false
    }).done(function (response) {
        //wyniki=[];
        wyniki="dlugosc,dB\n";
        for(var i=response["mini"];i<response["maxi"];i++){
            var pom2=response[String(i)];
            pom=[];
            //pom.push(parseInt(pom2["x"])/1000);
            //pom.push(parseInt(pom2["y"])/1000);
            //wyniki.push(pom);
            wyniki=wyniki+(String(parseInt(pom2["x"])/1000)+","+String(parseInt(pom2["y"])/1000)+"\n");
        }
        $.ajax({
            type: 'GET',
            url: url2+"/api/results/".concat(id),
            data: JSON.stringify(payload),
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST,GET,DELETE,PUT,OPTIONS',
                'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, Authorization',
                'Access-Control-Allow-Credentials': 'true'
            },
            contentType: "application/json",
            dataType: 'json',
            crossDomain: true
        }).success(function (response2){
            var pom3=response2[String(id)];
            var dystans=pom3["distance"];
            var impuls=pom3["pulse"];
            var comment=pom3["opis"];
            var eof_center=pom3["eof_center"];
            var eof_range=300;
            g3 = new Dygraph(
                document.getElementById("chart"),
                wyniki,
                {   //labels:["x","y"],
                    colors: ['#002B5E'],
                    //animatedZooms: true,
                    legend: 'follow',
                    showRangeSelector: true,
                    title: "Wynik ".concat(id)+'<br>'.concat(String(dystans))+'km'+'/'.concat(String(impuls))+'ns',
                    //ylabel: "Tłumienie (dB)"
                    underlayCallback: function(canvas, area, g) {
                        var highlight_start=parseInt(eof_center)-parseInt(eof_range);
                        var highlight_end=parseInt(eof_center)+parseInt(eof_range);
                        var bottom_left = g.toDomCoords(highlight_start/1000, -20);
                        var top_right = g.toDomCoords(highlight_end/1000, +20);
                        var left = parseInt(bottom_left[0]);
                        var right = parseInt(top_right[0]);
                        canvas.fillStyle = "rgba(255, 0, 0, 1.0)";
                        canvas.fillRect(left, area.y, right - left, area.h);
                    }
                });
            document.getElementById("trace_comment").value=comment;
        });

        //document.getElementById("trid").value=id;
        //document.getElementById(String(document.getElementById("trid").value)).style.backgroundColor="#ffffff";
        //document.getElementById("trid").value=id;
        //document.getElementById(String(id)).style.backgroundColor="#3B8BBA";
        document.getElementById("trace_lite").setAttribute('onclick','drawTrace('+String(id)+')');
        //document.getElementById("loader").style.zIndex= -10;
        //document.getElementById("loader").style.display="none";
    });
}

function aktualizujTrace(){
    var comment=document.getElementById("trace_comment").value;
    var trid=document.getElementById("trid").value;
    //console.log(trid);
    payload={"komentarz": String(comment)};
    $.ajax({
        type: 'POST',
        url: url2+"/api/results/".concat(trid),
        data: JSON.stringify(payload),
        headers: {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST,GET,DELETE,PUT,OPTIONS',
            'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, Authorization',
            'Access-Control-Allow-Credentials': 'true'
        },
        //success: function(data) { console.log(data);},
        contentType: "application/json",
        dataType: 'json',
        crossDomain: true
    }).success(function(){
        alert("Pomyślnie zastosowano zmiany");
    });
}

function usunTrace(){
    var trid=document.getElementById("trid").value;
    payload={"id": String(trid)};
    $.ajax({
        type: 'DELETE',
        url: url2+"/api/results/".concat(trid),
        data: JSON.stringify(payload),
        headers: {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST,GET,DELETE,PUT,OPTIONS',
            'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, Authorization',
            'Access-Control-Allow-Credentials': 'true'
        },
        //success: function(data) { console.log(data);},
        contentType: "application/json",
        dataType: 'json',
        crossDomain: true
    }).success(function(){
        location.reload();
    });
}

function exportToCSV(){
    var trid=document.getElementById("trid").value;
    $.ajax({
        type: 'GET',
        url: url2+"/api/trace/".concat(trid),
        data: JSON.stringify(payload),
        headers: {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST,GET,DELETE,PUT,OPTIONS',
            'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, Authorization',
            'Access-Control-Allow-Credentials': 'true'
        },
        //success: function(data) { console.log(data);},
        contentType: "application/json",
        dataType: 'json',
        crossDomain: true
    }).success(function (response) {
        wyniki=[];
        for(var i=response["mini"];i<response["maxi"];i++){
            var pom2=response[String(i)];
            pom=[];
            pom.push(String(parseInt(pom2["x"])/1000));
            pom.push(String(parseInt(pom2["y"])/1000));
            wyniki.push(pom);
        }

        var csvContent = "data:text/csv;charset=utf-8,";
        wyniki.forEach(function(infoArray, index){
            dataString = infoArray.join(",");
            csvContent += dataString + "\n";
        });
        var encodedUri = encodeURI(csvContent);
        var link = document.createElement("a");
        link.setAttribute("href", encodedUri);
        link.setAttribute("download", "Trace_"+String(trid)+".csv");
        document.body.appendChild(link);
        link.click();
    });
}

function refreshSite(){
    location.reload();
}

function filtruj(obiekt,port,dmin,dmax){
    if(String(obiekt)==''){
        obiekt="0";
    }
    if(String(port)==''){
        port="0";
    }
    if(String(dmin)==''){
        dmin="2010-01-01";
    }
    if(String(dmax)==''){
        dmax="2100-12-12";
    }
    payload={"eventy": "get"};
    $.ajax({
        type: 'GET',
        url: url2+"/api/wyniki/".concat(obiekt).concat("/").concat(port)+"/".concat(dmin)+"/".concat(dmax),
        data: JSON.stringify(payload),
        headers: {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST,GET,DELETE,PUT,OPTIONS',
            'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, Authorization',
            'Access-Control-Allow-Credentials': 'true'
        },
        //success: function(data) { console.log(data);},
        contentType: "application/json",
        dataType: 'json',
        async: false,
        crossDomain: true
    }).done(function (response) {
        var obiekt_nazwa;
        var licznik = response["licznik"];
        if(licznik>0){
            drawTrace(String(response["1"]["ID"]));
        }
        var Tabela = document.getElementById('wyniki-stats-data');
        Tabela.innerHTML = '';
        for (var i = 1; i <= licznik; i++) {
            var pom = response[String(i)];
            obiekt_nazwa=pom["nazwa"];
            var tr = document.createElement('TR');
            td1 = document.createElement('TD');
            var elem1 = document.createElement('c');
            elem1.appendChild(document.createTextNode(String(pom["ID"])));
            id=pom["ID"];
            elem1.setAttribute("onclick", 'drawTrace('+String(id)+')');
            td1.appendChild(elem1);
            tr.appendChild(td1);

            td2 = document.createElement('TD');
            td2.appendChild(document.createTextNode(String(pom["pulse"])));
            tr.appendChild(td2);

            td3 = document.createElement('TD');
            td3.appendChild(document.createTextNode(String(pom["distance"])));
            tr.appendChild(td3);

            td4 = document.createElement('TD');
            td4.appendChild(document.createTextNode(String(pom["eof_center"])));
            tr.appendChild(td4);

            Tabela.appendChild(tr);
            tr.setAttribute("id",String(pom["ID"]));
            tr = document.createElement('TR');

        }
        if(licznik>0){
            //drawTraceLite(String(response["1"]["ID"]));
            document.getElementById(String(response["1"]["ID"])).style.backgroundColor="#3B8BBA";
            //document.getElementById("trid").value=String(response["1"]["ID"]);
            document.getElementById("trace_lite").setAttribute('onclick','drawTrace('+String(response["1"]["ID"])+')')
        }
    });
}

function loadPage(){
    var g3 = new Dygraph(
        document.getElementById("chart"),
        [[0,0],[1,0]],
        {   labels:["x","y"],
            colors: ['#002B5E'],
            legend: "follow",
            //animatedZooms: true
        });
    filtruj(0,0,0,0);
}

function usunFiltr(){
    filtruj(0,0,0,0);
    document.getElementById("port_select").value='';
    document.getElementById("obiekt_select").value='';
    document.getElementById("date_select").value='';
    document.getElementById("date_select2").value='';
}

function reloadPage(){
    location.reload();
}

loadPage();
