import './style.css';
import {Map, View} from 'ol';
import TileLayer from 'ol/layer/Tile';
import OSM from 'ol/source/OSM';
import GeoTIFF from 'ol/source/GeoTIFF.js';

const tiff = new GeoTIFF({
  sources: [
    {
      url:'https://thenspe.github.io/P2306/Del2/imagery/AirPhotos/A02033-009.tif',
    },
  ],
})
const map = new Map({
  target: 'map',
  layers: [
    new TileLayer({
      source: new OSM()
    })
  ],
  view: new View({
    center: [0, 0],
    zoom: 2
  })
});
