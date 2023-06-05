// Create a Leaflet map
var map = L.map('map').setView([51.505, -0.09], 13);

// Add a base layer
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
    maxZoom: 18,
}).addTo(map);

// Load the GeoTIFF file
var url = 'Del2\imagery\TrentUniFreeTIFs\A02033-009_cog.tif';
fetch(url)
    .then(function(response) {
        return response.arrayBuffer();
    })
    .then(function(arrayBuffer) {
        // Create a GeoTIFF object from the array buffer
        return GeoTIFF.fromArrayBuffer(arrayBuffer);
    })
    .then(function(geotiff) {
        // Read the first image from the GeoTIFF
        return geotiff.getImage();
    })
    .then(function(image) {
        // Create a Leaflet GeoTIFF layer from the image
        var tiffLayer = L.leafletGeotiff(image).addTo(map);
        map.fitBounds(tiffLayer.getBounds());
    })
    .catch(function(error) {
        console.log('Error:', error);
    });
