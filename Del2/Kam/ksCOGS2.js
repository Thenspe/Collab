var parse_georaster = require("georaster");

var GeoRasterLayer = require("georaster-layer-for-leaflet");

// initalize leaflet map
var map = L.map('map').setView([45.000, -78.304], 8);

// add basemap layers
// OpenStreetMap
L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

const osm = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
});

// ESRI World Imagery
const Esri_WorldImagery = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
});

// Add baselayer info as array for layer control, control added lower to put it
// below the search bar
const baseLayers = {
  'OpenStreetMap': osm,
  'Esri World Imagery': Esri_WorldImagery
};

// // add geosearch control
// var geocoder = L.Control.geocoder({
//   collapsed: false,
//   position: 'topright',
//   defaultMarkGeocode: false
// }).on('markgeocode', function(result) {
//   const coords = [result.geocode.center.lat, result.geocode.center.lng];
//   var searchMarker = L.marker(coords, {
//       draggable: true //create draggable marker
//   }).addTo(map);
//   map.setView(coords,17);
// })
// .addTo(map);

//Add layer control button to switch between imagery and openstreetmap
const layerControl = L.control.layers(baseLayers).addTo(map);

// add air photo database geojson
var airphotos = L.geoJSON(photos, {
  onEachFeature: function (feature, info) {
      info.bindPopup('<p>Photo ID: '+feature.properties.PHOTO_ID+'</p>')
  }
}).addTo(map);

const url_to_geotiff_file = new URLSearchParams(location.search).get("url");
console.log("url_to_geotiff_file:", url_to_geotiff_file);

if (!url_to_geotiff_file) {
  setTimeout(function() {
    // if didn't pass in a url, redirect to planet example
    const parser = new URL(window.location);
    parser.searchParams.set("url", "https://ssfcollege-my.sharepoint.com/personal/ksandifo_flemingcollege_ca/_layouts/15/onedrive.aspx?listurl=https%3A%2F%2Fssfcollege%2Esharepoint%2Ecom%2Fsites%2FCollabTeam2306%2FShared%20Documents&viewid=5ce75b83%2D0ef9%2D4cfb%2D8f02%2D3e9b1d0bfcf5&login_hint=ksandifo%40flemingcollege%2Eca&id=%2Fsites%2FCollabTeam2306%2FShared%20Documents%2FGeneral%2Fimages%2FA16868%2D154%5FCOG%2ETIF&parent=%2Fsites%2FCollabTeam2306%2FShared%20Documents%2FGeneral%2Fimages");
    // "https://storage.googleapis.com/pdd-stac/disasters/hurricane-harvey/0831/20170831_172754_101c_3b_Visual.tif");
    window.location = parser.href;
  }, 2 * 1000);
} else {
  console.log("url_to_geotiff_file:", url_to_geotiff_file);
  parseGeoraster(url_to_geotiff_file).then(georaster => {
    console.log("georaster:", georaster);

    /*
        GeoRasterLayer is an extension of GridLayer,
        which means can use GridLayer options like opacity.

        Just make sure to include the georaster option!

        http://leafletjs.com/reference-1.2.0.html#gridlayer
    */
    var layer = new GeoRasterLayer({
        attribution: "Unknown",
        georaster,
            resolution: 128,
        airphotos,
            resolution: 128
        });
        layer.addTo(map);

        map.fitBounds(layer.getBounds());

      });
    }
