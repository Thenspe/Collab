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

const url_to_geotiff_file = new URLSearchParams(location.search).get("url");
console.log("url_to_geotiff_file:", url_to_geotiff_file);

if (!url_to_geotiff_file) {
  setTimeout(function() {
    // if didn't pass in a url, redirect to planet example
    const parser = new URL(window.location);
    parser.searchParams.set("url", "https://github.com/Thenspe/P2306/blob/main/Del2/imagery/AirPhotos/A02033-009.tif");

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
        });
        layer.addTo(map);

        map.fitBounds(layer.getBounds());

      });
    }
