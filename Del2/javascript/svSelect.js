/*
    FlemSem3\Collab\P2306\Del2
    python -m http.server

    This file adds a geoJson using JQuery
*/

// enable Turf.js for geospatial analysis later
const turf = require('@turf/turf');
const booleanOverlap = require('@turf/boolean-overlap');

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

// var showjson = L.FeatureGroup();
var photoJSON = L.geoJSON(null,{
    style: function(feature) {
        return {
            color: 'purple'
        }
    }
}).addTo(map); // Variable to hold the GeoJSON data
var sameJson;
  
$.getJSON('../geojson/aerials.json', function(data) {
    photoJSON.addData(data);
    sameJson = data;
    // photoJSON = data; // Assign the loaded GeoJSON data to the variable
    // L.geoJSON(photoJSON,{   //leaflet call for the geojson
    //     style: function(feature) {
    //         return {
    //             color: 'yellow' // make the polygons yellow
    //         }
    //     }
    // }).addTo(map);
    console.log(sameJson.features[1].properties) // for troubleshooting and viewing properties

    sameJson.features.sort(function(a,b) { // sort the JSON so it shows up nicely
        var propA = a.properties.PHOTO_ID;
        var propB = b.properties.PHOTO_ID;
        return propA - propB;
// .sort() orders by putting the lower number first, so if A - B is negative, A preceeds, if positive, B preceeds, if 0 they are equal
    });

    var outputList = $('#jsonResults'); // HTML ID to put the results into
    outputList.append('<h3>Available Photos</h3>'); // title for the list of results
    
    sameJson.features.forEach(function(feature) {
        var properties = feature.properties;
        outputList.append('<input type="checkbox">')
        outputList.append('<label> ' + properties.PHOTO_ID + '</label></br>');
    });
});
baseControl.addOverlay(photoJSON,"Aerial Image Locations");

var userIn = new L.FeatureGroup().addTo(map);  // variable to store user drawn inputs

// add drawing control bar
var drawControl = new L.Control.Draw({
    draw: {
        polygon: true,
        polyline: false,
        rectangle: false,
        circle: false,
        circlemarker: false,
        marker: true,
    },
    edit: {
        featureGroup: userIn
    }
});
map.addControl(drawControl);

// save user drawn items as new layers in the layer group
map.on('draw:created', function(e) {
    var layer = e.layer;
    userIn.addLayer(layer);
});

// check the user-polygon for image overlap
function checkForPhotos() {
    if (userIn === null) {
        console.log('Draw a thing.');
    }
    // you left off here. Getting into Turf.js - see if you can get a build that just includes booleanOverlap 
}