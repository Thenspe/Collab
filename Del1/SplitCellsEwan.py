import arcpy
# Set workspace (update to your own workspace file path)
arcpy.env.workspace = r"C:\Courses\GEOM68\Sandbox\GEOM68_WellWaterDB\Default.gdb"

tbl = r"Wells_Report_ExportTable"

# Define the new fields to populate the split values
# arcpy.AddField_management(tbl, "WellID", "TEXT")
# arcpy.AddField_management(tbl, "GEO1", "TEXT")
# arcpy.AddField_management(tbl, "GEO2", "TEXT")
# arcpy.AddField_management(tbl, "GEO3", "TEXT")
# arcpy.AddField_management(tbl, "GEO4", "TEXT")
# arcpy.AddField_management(tbl, "GEO5", "TEXT")
# arcpy.AddField_management(tbl, "GEO6", "TEXT")
# arcpy.AddField_management(tbl, "GEO7", "TEXT")
# arcpy.AddField_management(tbl, "GEO8", "TEXT")
# arcpy.AddField_management(tbl, "GEO9", "TEXT")

# Define the parameters for the UpdateCursor() function to iterate through the feature class 
# to split the string value based on a delimiter and remove leading and trailing blank spaces in the new fields.
with arcpy.da.UpdateCursor(tbl, ["GEO", "GEO1", "GEO2", "GEO3", "GEO4", "GEO5", "GEO6"]) as cursor:
    
    for row in cursor:
        entries = len(row[0].split("|"))
    x = 0

    while x != entries:
        row[x+1]=row[0].split("|")[x]
        x+1
       
        row=[i.strip() if i is not None else None for i in row]
        cursor.updateRow(row)
