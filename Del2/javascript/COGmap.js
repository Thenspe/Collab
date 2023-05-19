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
    center: [44.340, -78.741], //45.000, -78.304 for ontario
    zoom: 12,
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

/*
// add air photo database geojson
var airphotos = L.geoJSON(photos, {
    onEachFeature: function (feature, info) {
        info.bindPopup('<p>Photo ID: '+feature.properties.PHOTO_ID+'</p>')
    }
}).addTo(map);
*/

var image1URL = 'images/A16868_154.png';
var imageErrorOverlayUrl = 'https://cdn-icons-png.flaticon.com/512/110/110686.png';
var altText = 'alternative text';
var image1Bounds = L.latLngBounds([[44.385133704289053, -78.745641039671753], [44.325644754986556, -78.659455982686808]]);

var image1overlay = L.imageOverlay(image1URL,image1Bounds, {
    errorOverlayURL: imageErrorOverlayUrl,
    alt: altText
}).addTo(map);  

const cog1url = "images/A18773-025_COG.TIF";
const options = {
    renderer: L.LeafletGeotiff.rgb,
    useWorker: false,
    bounds: [],
    band: 0,
    image: 0,
    clip: undefined,
    pane: "overlayPane",
    onError: null,
    sourceFunction: GeoTIFF.fromUrl,
    arrayBuffer: null,
    noDataValue: undefined,
    noDataKey: undefined,
    // The block size to use for buffer
    blockSize: 65536,
    // Optional, override default opacity of 1 on the image added to the map
    opacity: 1,
    // Optional, hide imagery while map is moving (may prevent 'flickering' in some browsers)
    clearBeforeMove: false,
};
const cog1layer = L.leafletGeotiff(cog1url, options).addTo(map);