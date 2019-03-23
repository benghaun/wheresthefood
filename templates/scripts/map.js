var infowindow;
var map;
function addMarker (markerarray,marker){
    markerarray[markerarray.length]=marker;
};

function createMarker(string,latlng){
    var marker=new google.maps.Marker({position:latlng,map:map});
    google.maps.event.addListener(marker,"click",function(){
        if(infowindow)infowindow.close();
        infowindow=new google.maps.InfoWindow({content:string});
        infowindow.open(map,marker);
    });
    return marker;
};

function initMap(){
    var singapore=new google.maps.LatLng(1.35,103.82);
    var options={zoom:11,center:singapore};
    map=new google.maps.Map(document.getElementById("map"),options);
    map.discmarkers=new Array();

    $.ajax({
        url: "/getdeals",
        method: "GET",
        dataType: "json",
        data: {},
        complete: function(xhr, status) {},
        success: function(data, status, xhr) {
            for(var i=0;i<data.length;i++){
                var card = new Object();
                card.name = data[i].name;
                card.enddate = data[i].enddate;
                card.timeinfo = (data[i].timeinfo)? data[i].timeinfo:'';
                card.timeinfo = '<br><br>'+card.timeinfo;
                card.latlongs = data[i].latlongs;
                var contentString = '<div id="infoview">'+
                '<p><b>'+ card.name + '</b><br>' +
                'Until '+ card.enddate.substring(0, card.enddate.length-13) +
                card.timeinfo +
                '</p></div>'
                for(var j=0;j<card.latlongs.length;j++){
                    var latlng=new google.maps.LatLng(card.latlongs[j][0],card.latlongs[j][1]);
                    addMarker(map.discmarkers,createMarker(contentString,latlng));
                }
                
            }
        }
    });
};

$(document).ready(function() {
    $("#zoomarea").click(function() {
        var area = $("#zoominput").val();
        var urlString = "/viewport?search=" + area;
        $.ajax({
            url: urlString,
            method: "GET",
            dataType: "json",
            data: {},
            complete: function(xhr, status) {},
            success: function(data, status, xhr) {
                var bounds = new google.maps.LatLngBounds(data.results.southwest,data.results.northeast)
                map.fitBounds(bounds);
            }
        });
    });
    
    $("#zoominput").on("keydown", function(e) { 
        if(e.keyCode == 13)
            $("#zoomarea").click() 
    });
}); 