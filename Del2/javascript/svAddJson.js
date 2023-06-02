/*
    FlemSem3\Collab\P2306\Del2
    python -m http.server

    This file adds a geoJson using JQuery
*/
// Add map baselayers
const osm = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
});
const Esri_WorldImagery = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
});
//Map declaration
const map = L.map('map', {
    center: [44.3, -77.8],    //44.5, -78
    zoom: 12,
    layers: [Esri_WorldImagery,osm]            
});
// Add baselayer info as array for layer control, control added lower to put it
// below the search bar
const baseLayers = {
    'Esri World Imagery': Esri_WorldImagery,
    'OpenStreetMap': osm
};
const baseControl = L.control.layers(baseLayers,null,{position:'topleft'}).addTo(map);

var photoJSON; // Variable to hold the GeoJSON data
  
$.getJSON('../geojson/aerials.json', function(data) {
    photoJSON = data; // Assign the loaded GeoJSON data to the variable
    L.geoJSON(photoJSON,{
        style: function(feature) {
            return {
                color: 'yellow'
            }
        }
    }).addTo(map);
    console.log(photoJSON.features[1].properties)
    for (var photos in photoJSON.features)
        $('section[id="jsonResults"]').append('<p>' + photoJSON.features[photos].properties.PHOTO_ID + '</p>');
});