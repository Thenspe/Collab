# import arcpy
# # Set workspace (update to your own workspace file path)
# arcpy.env.workspace = "C:\Courses\GEOM68\Sandbox\GEOM68_WellWaterDB\Default.gdb"

# tbl = "Wells_Report_ExportTable"

# # Define the new fields to populate the split values
# # arcpy.AddField_management(tbl, "WellID", "TEXT")
# # arcpy.AddField_management(tbl, "GEO1", "TEXT")
# # arcpy.AddField_management(tbl, "GEO2", "TEXT")
# # arcpy.AddField_management(tbl, "GEO3", "TEXT")
# # arcpy.AddField_management(tbl, "GEO4", "TEXT")
# # arcpy.AddField_management(tbl, "GEO5", "TEXT")
# # arcpy.AddField_management(tbl, "GEO6", "TEXT")
# # arcpy.AddField_management(tbl, "GEO7", "TEXT")
# # arcpy.AddField_management(tbl, "GEO8", "TEXT")
# # arcpy.AddField_management(tbl, "GEO9", "TEXT")

# # Define the parameters for the UpdateCursor() function to iterate through the feature class 
# # to split the string value based on a delimiter and remove leading and trailing blank spaces in the new fields.
# with arcpy.da.UpdateCursor(tbl, ["GEO", "GEO1", "GEO2", "GEO3", "GEO4", "GEO5", "GEO6", "GEO7", "GEO8", "GEO9"]) as cursor:
    
#     for row in cursor:         
#         row[1] = row[0].split("|")[0]
#         row[2] = row[0].split("|")[1]
#         row[3] = row[0].split("|")[2]
#         row[4] = row[0].split("|")[3]
#         row[5] = row[0].split("|")[4]
#         row[6] = row[0].split("|")[5]
#         row[7] = row[0].split("|")[6]
#         row[8] = row[0].split("|")[7]
#         row[9] = row[0].split("|")[8]

        # row=[i.strip() if i is not None else None for i in row]
        # cursor.updateRow(row)

import arcpy

workspace="C:\Courses\GEOM68\Sandbox\CollabProj.gdb"
arcpy.env.workspace = workspace

bhResultsTable = 'Borehole_Results'
# check if the table already exists, remove it if it does.
if arcpy.Exists(bhResultsTable):
    print('Table exists, deleting...')
    arcpy.Delete_management(bhResultsTable)
    print('Table deleted.')
print("Creating table.")
# create the table
arcpy.management.CreateTable(workspace,bhResultsTable)
# set the fields for the new table
insertFields = ['Well_ID','Colour','Mat1','Mat2','Mat3','Top','Bot']
# add fields to the table
arcpy.management.AddFields(bhResultsTable,
    [[insertFields[0],'LONG',None,15],
     [insertFields[1],'TEXT','Colour',15],
     [insertFields[2],'TEXT','Material 1',15],
     [insertFields[3],'TEXT','Material 2',15],
     [insertFields[4],'TEXT','Material 3',15],
     [insertFields[5],'TEXT','Top of Layer',15],
     [insertFields[6],'TEXT','Bottom of Layer',15]])

# set the relevant fields from the table with the data
searchFields = ['Well_ID','GEO']
# create the insert cursor, for populating the new table
addStuff = arcpy.da.InsertCursor('Borehole_Results', insertFields)
# create the search cursor, for pulling data from the original table
pull = arcpy.da.SearchCursor('Wells_In_Buffer', searchFields)
for row in pull:                # for each row in the original table...
    # print(pull)
    pipes = pull[1].split("|")  # separate by the pipes.
    # print(pipes)
    for x in pipes:             # for each set of pipes...
        semicolons = x.split(";")   # separate by the semicolons.
        # print(pull[0])
        # print(len(semicolons))
        if len(semicolons) > 1:     # only add lines that have values in them
            addStuff.insertRow([pull[0],semicolons[0],semicolons[1],semicolons[2],semicolons[3],semicolons[4],semicolons[5]])
            # print(semicolons)
del pull        # close the cursors to prevent errors
del addStuff
print('Process complete.')  # Good job, script!
