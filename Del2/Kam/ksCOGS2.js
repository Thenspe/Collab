var parse_georaster = require("georaster");

var GeoRasterLayer = require("georaster-layer-for-leaflet");

// initalize leaflet map
var map = L.map('map').setView([0, 0], 5);

// add OpenStreetMap basemap
L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

const url_to_geotiff_file = new URLSearchParams(location.search).get("url");
console.log("url_to_geotiff_file:", url_to_geotiff_file);

if (!url_to_geotiff_file) {
  setTimeout(function() {
    // if didn't pass in a url, redirect to planet example
    const parser = new URL(window.location);
    parser.searchParams.set("url", "https://storage.googleapis.com/pdd-stac/disasters/hurricane-harvey/0831/20170831_172754_101c_3b_Visual.tif");
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
            resolution: 128
        });
        layer.addTo(map);

        map.fitBounds(layer.getBounds());

      });

      var items = [];
      var at_states = L.geoJson(at, {
        onEachFeature: function(data, layer) {
          items.push(layer);
          layer.bindPopup('<b>' + data.properties.name + '</b><br>'
            + data.properties.cities + ' Cities'+'<br>'
            + data.properties.towns + ' Towns'+'<br>'
            + data.properties.density + ' People / km<sup>2</sup>');
        }
      }).addTo(map);
      
      var baseLayers = {
        "ESRI World Imagery": esri_WorldImagery,
        "ESRI World Terrain": esri_WorldTerrain
      };
      
      var overLayers = {
        "Austrian States": at_states
      }
      
      L.control.layers(baseLayers, overLayers).addTo(map);
      L.control.search({data: items}).addTo(map);

    }
