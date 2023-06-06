// initalize leaflet map
var map = L.map('map').setView([44.299999, -78.316666], 12);

// 44.299999, -78.316666 -Peterborough

// 45.000, -78.304 

// add basemap layers
// OpenStreetMap
var osm_streetmap = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Osm Topographics
var osm_topo = L.tileLayer('http://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
	maxZoom: 17,
	attribution: 'Map data: &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)'
});

// ESRI World Imagery
var Esri_WorldImagery = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
});

// Display the raster image - tif, geotiff, cog.
var url_to_geotiff_file = 'http://127.0.0.1/images/CAP/Whitby2.tif'

parseGeoraster(url_to_geotiff_file).then(georaster => {
  console.log("georaster:", georaster)

  /*
      GeoRasterLayer is an extension of GridLayer,
      which means can use GridLayer options like opacity.

      Just make sure to include the georaster option!

      http://leafletjs.com/reference-1.2.0.html#gridlayer
  */
  var layer = new GeoRasterLayer({
      attribution: "Whitby",
      georaster: georaster,
      resolution: 256
  });
  layer.addTo(map);

  map.fitBounds(layer.getBounds());

});

// Load the polygon via the geoJSON files
var polydata = L.geoJSON(APpoly3,{
  onEachFeature: function(feature,layer){
    layer.bindPopup('<b>This is photo </b>' + feature.properties.PHOTO_ID)
  },
  style:{
    fillColor: 'red',
    fillOpacity: 1,
    color: 'green'
  }
}).addTo(map);

// Add the map Layer Control
// Baselayers
var baseLayers = {
  "OSM Streets": osm_streetmap,
  "OSm Topo": osm_topo,
  "ESRI World Imagery": Esri_WorldImagery,
};

// airphoto polygons
var polygons = {
  "Air Photo Polygons": polydata,
};

// Add layer control to map
L.control.layers(baseLayers, polygons).addTo(map);

L.control.layers(layer, null).addTo(map);
