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
arcpy.conversion.ExportTable(in_table=bufferedTable,out_table=typeTable,use_field_alias_as_name=True,field_mapping=[
    'WELL_ID',
    'WELL_COMPLETED_DATE',
    'RECEIVED_DATE',
    'TAG',
    'SWL',
    'FINAL_STATUS_DESCR',
    'USE1',
    'USE2',
    'UTMZONE',
    'EAST83',
    'NORTH83',
    'PT',
    'DEPTH_M'
])
# set the fields for the new table
# insertFields = ['Well_ID','Colour','Mat1','Mat2','Mat3','Top','Bot']
# add fields to the table
# arcpy.management.AddFields(bhResultsTable,
#     [[insertFields[0],'LONG',None,15],
#      [insertFields[1],'TEXT','Colour',15],
#      [insertFields[2],'TEXT','Material 1',15],
#      [insertFields[3],'TEXT','Material 2',15],
#      [insertFields[4],'TEXT','Material 3',15],
#      [insertFields[5],'TEXT','Top of Layer',15],
#      [insertFields[6],'TEXT','Bottom of Layer',15]])


print('Process complete.')