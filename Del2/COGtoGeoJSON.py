from osgeo import ogr

# Input .vrt file path
input_vrt_file = 'input.vrt'

# Output shapefile path
output_shapefile = 'output.shp'

# Open the .vrt file
vrt_ds = ogr.Open(input_vrt_file)

# Get the first layer from the .vrt file
vrt_layer = vrt_ds.GetLayer()

# Create a new shapefile and define its geometry type
driver = ogr.GetDriverByName('ESRI Shapefile')
output_ds = driver.CreateDataSource(output_shapefile)
output_layer = output_ds.CreateLayer('layer_name', srs=None, geom_type=vrt_layer.GetGeomType())

# Copy the fields from the .vrt layer to the shapefile layer
vrt_layer_defn = vrt_layer.GetLayerDefn()
for i in range(vrt_layer_defn.GetFieldCount()):
    field_defn = vrt_layer_defn.GetFieldDefn(i)
    output_layer.CreateField(field_defn)

# Copy the features from the .vrt layer to the shapefile layer
for feature in vrt_layer:
    output_layer.CreateFeature(feature)

# Clean up and close the data sources
output_ds = None
vrt_ds = None
