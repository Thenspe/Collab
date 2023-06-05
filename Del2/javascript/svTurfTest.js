//just checkign if my turf build worked
// var bbox = turf.bbox(features);

const polygon1 = turf.polygon([[[0, 0], [0, 10], [10, 10], [10, 0], [0, 0]]]);
const polygon2 = turf.polygon([[[5, 5], [5, 15], [15, 15], [15, 5], [5, 5]]]);

const overlap = booleanOverlap(polygon1, polygon2);
console.log('Do the polygons overlap?', overlap);
