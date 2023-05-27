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
    layers: [osm, Esri_WorldImagery]            
});
// Add baselayer info as array for layer control, control added lower to put it
// below the search bar
const baseLayers = {
    'Esri World Imagery': Esri_WorldImagery,
    'OpenStreetMap': osm
};

// add geosearch control
var geocoder = L.Control.geocoder({
    collapsed: false,       // keep it large
    position: 'topright',   // put it in the upper right corner
    defaultMarkGeocode: false
}).on('markgeocode', function(result) {
    const coords = [result.geocode.center.lat, result.geocode.center.lng]; 
    var searchMarker = L.marker(coords, {
        draggable: true //create draggable marker
    }).addTo(map);
    map.setView(coords,17); // move the map view to the searched location
})
.addTo(map);

//Add layer control button to switch between imagery and openstreetmap
const baseControl = L.control.layers(baseLayers,null,{position:'topleft'}).addTo(map);

/////////////////////////////////////////////////////////////////////////////////////////
// This section attempts to add a control to filter by decade

// var layerInfo = {
//     twenties: {source:"192", color: '#FE1A1A'},
//     thirties: {source:"193", color: '#FEAB1A'},
//     fourties: {source:"194", color: '#FEFE1A'},
//     fifties: {source:"195", color: '#82FE1A'},
//     sixties: {source:"196", color: '#32AE0E'},
//     seventies: {source:"197", color: '#1AFE89'},
//     eighties: {source:"198", color: '#1AFEFB'},
//     nineties: {source:"199", color: '#1A63FE'},
//     aughts: {source:"200", color: '#891AFE'},
//     ohtens: {source:"201", color: '#FE1AFB'},
//     ohtwenties: {source:"202", color: '#FE1A96'}
// };

// var geoJsonLayers = {}; //to put the geojson into

// for(var layer in layerInfo) {
//     geoJsonLayers[layer] = L.geoJSON(airphotopoly, {
//         filter: function(feature) {
//             if(feature.properties.date[layerInfo[layer].source] == feature.properties.date.slice(0,2)) {
//                 return true;
//             }
//         },
//         style: function(feature) {
//             return {
//                 color: layerInfo[layer].color
//             }
//         },
//         onEachFeature: function (feature, info) { 
//             info.bindPopup('<p>Photo ID: '+feature.properties.PHOTO_ID+'</p>'+'<p>Photo Date: '+feature.properties.Photo_Date+'</p>')
//         }
//     }).addTo(map);
// }

// var sourcesLabels = {
//     "1920's": geoJsonLayers.twenties,
//     "1930's": geoJsonLayers.thirties,
//     "1940's": geoJsonLayers.fourties,
//     "1950's": geoJsonLayers.fifties,
//     "1960's": geoJsonLayers.sixties,
//     "1970's": geoJsonLayers.seventies,
//     "1980's": geoJsonLayers.eighties,
//     "1990's": geoJsonLayers.nineties,
//     "2000's": geoJsonLayers.aughts,
//     "2010's": geoJsonLayers.ohtens,
//     "2020's": geoJsonLayers.ohtwenties
// };

// // add layer control for sorting through the geojson
// var imageControl = L.control.layers(null,sourcesLabels, {collapsed:false,position:'topright'}).addTo(map);
// // this control needs to:
// //  - show items from the geojson
// //  - restrict based on what is visible

/////////////////////////////////////////////////////////////////////////////////////////
// this section attempts to filter by map bounds

airVectors = L.geoJSON(airphotopoly, {  // add the geoJSON
    style: function(feature) {
        return {color: 'yellow'}    // and select the colour
    }
}).bindPopup(function (layer) {
    return layer.feature.properties.date.slice(0,3);
})//.addTo(map);;

// add a button to summon photos on a drawn layer or point
var ourCustomControl = L.Control.extend({
    options: {
        position: 'topright'
    },
    onAdd: function (map) {
        var container = L.DomUtil.create('button'); 

        container.innerText = 'Find Aerial Imagery';
        
        container.style.backgroundColor = 'white';
        container.style.borderWidth = '2px';
        container.style.borderColor = '#b4b4b4';
        container.style.borderRadius = '5px';
        container.style.borderStyle = 'solid';
        container.style.width = '140px';
        container.style.height = '30px';
        
        container.onclick = function(){
            var drawnLayers = map.pm.getGeomanLayers(true);
            console.log('Button has been clicked.');
            console.log(drawnLayers);

        }
        return container;
    },
});
map.addControl(new ourCustomControl());

//add the drawing toolbar
map.pm.addControls({
    position: 'topleft',
    drawCircle: false,
    drawCircleMarker: false,
    drawRectangle: false
});
map.pm.setPathOptions(
    {color: 'red'}
);
// var drawnLayers = map.pm.getGeomanLayers();
// console.log(drawnLayers);