# Stephen's space for messing around with Python

import arcpy

workspace="D:\\FlemSem3\\Collab\\CollabProj\\CollabProj.gdb"
arcpy.env.workspace = workspace

bufferedTable = 'Wells_In_Buffer'
typeTable = 'Well_Type'
# check if the table already exists, remove it if it does.
if arcpy.Exists(typeTable):
    print(typeTable + ' table exists, deleting...')
    arcpy.Delete_management(typeTable)
    print('Table deleted.')
print("Creating table.")

# create the table
arcpy.management.CreateTable(workspace,typeTable)
# set the fields for the new table
insertFields = ['WELL_ID','TAG','EAST83','NORTH83','UTMZONE','WELL_COMPLETED_DATE','RECEIVED_DATE','FINAL_STATUS_DESCR','USE1','USE2','DEPTH_M','WAT','SWL','PT']
# add fields to the table
for x in insertFields:
    arcpy.management.AddField(typeTable,x,'TEXT')


print('Process complete.')