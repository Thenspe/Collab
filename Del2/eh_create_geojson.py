# import os
# import subprocess

# # Directory path containing COGs
# cog_dir = 'C:\Courses\GEOM68\Sandbox\Del2\TrentUniFreeCOGs'

# # Output GeoJSON file path
# output_geojson = 'C:\Courses\GEOM68\Sandbox\Del2\TrentUniFreeCOGs\TrentCOG.geojson'

# # Get a list of COG files in the directory
# cog_files = [os.path.join(cog_dir, file) for file in os.listdir(cog_dir) if file.endswith('.tif')]

# # Create a VRT file from the COG files
# vrt_file = 'temp.vrt'
# subprocess.run(['rio', 'mosaic', *cog_files, '--output', vrt_file])

# # Convert VRT to GeoJSON using rio
# subprocess.run(['rio', 'info', vrt_file, '--as-json', '--indent', '2', '--bounds', '--formats', 'GeoJSON', '--output', output_geojson])

# # Clean up the temporary VRT file
# os.remove(vrt_file)

# print(f"GeoJSON file created: {output_geojson}")

# import os
# import json
# import rasterio
# from rasterio.transform import Affine
# from rasterio.warp import transform_bounds

# # Directory containing the COG files
# directory = "/path/to/cog_directory"

# # Create an empty feature collection
# feature_collection = {
#     "type": "FeatureCollection",
#     "features": []
# }

# # Iterate through the directory
# for filename in os.listdir(directory):
#     if filename.endswith(".tif") or filename.endswith(".tiff"):
#         cog_path = os.path.join(directory, filename)

#         # Open the COG file and read the metadata
#         with rasterio.open(cog_path) as dataset:
#             bounds = dataset.bounds
#             crs = dataset.crs.to_string()

#         # Transform the bounds to WGS84 (EPSG:4326)
#         transform = Affine.from_gdal(*dataset.transform)
#         wgs84_bounds = transform_bounds(transform, *bounds)

#         # Create a feature for the COG file
#         feature = {
#             "type": "Feature",
#             "properties": {
#                 "filename": filename
#             },
#             "geometry": {
#                 "type": "Polygon",
#                 "coordinates": [[
#                     [wgs84_bounds[0], wgs84_bounds[1]],
#                     [wgs84_bounds[0], wgs84_bounds[3]],
#                     [wgs84_bounds[2], wgs84_bounds[3]],
#                     [wgs84_bounds[2], wgs84_bounds[1]],
#                     [wgs84_bounds[0], wgs84_bounds[1]]
#                 ]]
#             }
#         }

#         # Add the feature to the feature collection
#         feature_collection["features"].append(feature)

# # Save the GeoJSON file
# output_file = "/path/to/output.geojson"
# with open(output_file, "w") as f:
#     json.dump(feature_collection, f)

# print("GeoJSON file saved successfully.")

import rasterio

try:
    import rasterio
    print("rasterio is installed.")
    print("Version:", rasterio.__version__)
except ImportError:
    print("rasterio is not installed.")
