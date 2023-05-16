# This script creates the Wells_Type table from Wells_In_Buffer, because ModelBuilder keeps losing the field maps.
# It doesn't use field mapping, that is a bag of hurt.

import arcpy

workspace="D:\\FlemSem3\\Collab\\CollabProj\\CollabProj.gdb"
arcpy.env.workspace = workspace
arcpy.env.overwriteOutput = True

def addSomeFields(table,field,alias):
    x = 0
    while x < len(field):
        fieldLength = 20
        if field[x] == 'FINAL_STATUS_DESCR' or field[x] == 'USE1' or field[x] == 'USE2' or field[x] == 'WAT':
            fieldLength = 100
        else:
            fieldLength = 20
        arcpy.management.AddField(table,field[x],'TEXT',field_length=fieldLength,field_alias=alias[x],field_is_nullable=False)
        x+=1

dataTable = 'Wells_In_Buffer'
tables = ['Wells_Type','Borehole_Results','Borehole_Details']
t = 0
while t < len(tables):
    if arcpy.Exists(tables[t]):
        print("Table",tables[t],"exists, deleting . . .")
        arcpy.Delete_management(tables[t])
        print("Table",tables[t],"deleted.")
    print("Creating table",tables[t],". . .")
    arcpy.management.CreateTable(workspace,tables[t])
    print("Table",tables[t],"created.")
    print()

    tableFields = [
        #well_type
        ['WELL_ID','TAG','EAST83','NORTH83','UTMZONE','WELL_COMPLETED_DATE','RECEIVED_DATE','FINAL_STATUS_DESCR','USE1','USE2','DEPTH_M','WAT','SWL','PT','RPR','PUMPDUR'],
        # borehole_results
        ['WELL_ID','Colour','Mat1','Mat2','Mat3','Top','Bot'],
        # borehole_details
        ['WELL_ID','HOLE_D','HOLE_T','HOLE_B','CAS_M','CAS_D','CAS_T','CAS_B','SCRN_D','SCRN_M','SCRN_T','SCRN_B']
    ]
    tableAlias = [
        # well_type
        ['Well ID','TAG','Easting','Northing','UTM Zone','Well Completion Date','Received Date','Final Status','Use 1','Use 2','Well Depth','Water First Found','Static Water Level','PT','Recommended Pump Rate','Pump Duration'],
        # borehole_results
        ['Well ID','Colour','Material 1','Material 2','Material 3','Upper limit','Lower limit'],
        # borehole_details
        ['Well ID','Hole Diameter','Hole Top','Hole Bottom','Casing Material','Casing Casing Diameter','Casing Top','Casing Bottom','Screen Diameter','Screen Material','Screen Top','Screen Bottom']
    ]

    addSomeFields(tables[t],tableFields[t],tableAlias[t])
    t+=1


print('Process complete.')

