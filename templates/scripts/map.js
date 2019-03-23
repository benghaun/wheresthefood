var infowindow;
var map;
function addMarker (marker){
    map.markers[map.markers.length]=marker;
};

function getMarkers(){
        return map.markers
};

function createMarker(name,latlng){
    var marker=new google.maps.Marker({position:latlng,map:map});
    google.maps.event.addListener(marker,"click",function(){
        if(infowindow)infowindow.close();
        infowindow=new google.maps.InfoWindow({content:name});
        infowindow.open(map,marker);
    });
    return marker;
};

function initMap(){
    var singapore=new google.maps.LatLng(1.35,103.82);
    var options={zoom:11,center:singapore};
    map=new google.maps.Map(document.getElementById("map"),options);
    map.markers=new Array();

    var a=new Array();
    
    var t=new Object();
    t.name="Bugis Junction"
    t.lat=1.29886
    t.lng=103.855548
    a[0]=t;
    
    var t=new Object();
    t.name="Eastpoint"
    t.lat=1.342715
    t.lng=103.953041
    a[1]=t;
    
    var t=new Object();
    t.name="Yishun Townsquare"
    t.lat=1.427383
    t.lng=103.836699
    a[2]=t;
    
    for(var i=0;i<a.length;i++){
        var latlng=new google.maps.LatLng(a[i].lat,a[i].lng);
        addMarker(createMarker(a[i].name,latlng));
    }
    console.log(getMarkers());
};

$(document).ready(function() {
    $("#zoomarea").click(function() {
        var area = $("#zoominput").val();
        var urlString = "http://127.0.0.1:5000/viewport?search=" + area;
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