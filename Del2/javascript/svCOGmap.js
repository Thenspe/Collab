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
    center: [45.000, -78.304],
    zoom: 8,
    layers: [osm, Esri_WorldImagery]            
});
// Add baselayer info as array for layer control, control added lower to put it
// below the search bar
const baseLayers = {
    'OpenStreetMap': osm,
    'Esri World Imagery': Esri_WorldImagery
};

// add geosearch control
var geocoder = L.Control.geocoder({
    collapsed: false,
    position: 'topright',
    defaultMarkGeocode: false
}).on('markgeocode', function(result) {
    const coords = [result.geocode.center.lat, result.geocode.center.lng];
    var searchMarker = L.marker(coords, {
        draggable: true //create draggable marker
    }).addTo(map);
    map.setView(coords,17);
})
.addTo(map);

//Add layer control button to switch between imagery and openstreetmap
const layerControl = L.control.layers(baseLayers).addTo(map);

// var showMeAirPhotos = L.geoJSON()

// add air photo database geojson
var airphotos = L.geoJSON(photos, {
  style: function(feature) {
    return {color: 'blue'};
  },
  onEachFeature: function (feature, info) {
      info.bindPopup('<p>Photo ID: '+feature.properties.PHOTO_ID+'</p>')
  }
}).addTo(map);
var airphotos2 = L.geoJSON(airpoly, {
  style: function(feature) {
    return {color: 'red'};
  },
  onEachFeature: function (feature, info) {
      info.bindPopup('<p>Photo ID: '+feature.properties.PHOTO_ID+'</p>'+'<p>Photo Date: '+feature.properties.Photo_Date+'</p>')
  }
}).addTo(map);