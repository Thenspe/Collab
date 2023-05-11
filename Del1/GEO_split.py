# This script creates the Borehole_Results table
# and splits the field GEO into it

# example_data = ""
example_data = "BRWN ;SAND ;CLAY ;FILL ;0 m;2.43 m|BRWN ;CLAY ;SILT ; DRY ;2.43 m;3.65 m|BRWN ;SAND ;STNS ;WBRG ;3.65 m;4.57 m|"
# example_data = "40 ft"
# example_data = "6 m"

import arcpy

workspace="D:\\FlemSem3\\Collab\\CollabProj\\CollabProj.gdb"
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
