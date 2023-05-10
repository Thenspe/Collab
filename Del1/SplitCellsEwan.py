import arcpy
# Set workspace (update to your own workspace file path)
arcpy.env.workspace = "C:\Courses\GEOM68\Sandbox\GEOM68_WellWaterDB\Default.gdb"

tbl = "Wells_Report_ExportTable"

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
with arcpy.da.UpdateCursor(tbl, ["GEO", "GEO1", "GEO2", "GEO3", "GEO4", "GEO5", "GEO6", "GEO7", "GEO8", "GEO9"]) as cursor:
    
    for row in cursor:         
        row[1] = row[0].split("|")[0]
        row[2] = row[0].split("|")[1]
        row[3] = row[0].split("|")[2]
        row[4] = row[0].split("|")[3]
        row[5] = row[0].split("|")[4]
        row[6] = row[0].split("|")[5]
        row[7] = row[0].split("|")[6]
        row[8] = row[0].split("|")[7]
        row[9] = row[0].split("|")[8]

        row=[i.strip() if i is not None else None for i in row]
        cursor.updateRow(row)
