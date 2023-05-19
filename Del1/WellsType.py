# this script populates the table Well_Type

import arcpy

workspace="D:\\FlemSem3\\Collab\\CollabProj\\CollabProj.gdb"
arcpy.env.workspace = workspace

# try:
searchFields = ['WELL_ID','TAG','EAST83','NORTH83','UTMZONE','WELL_COMPLETED_DATE','RECEIVED_DATE','FINAL_STATUS_DESCR','USE1','USE2','DEPTH_M','WAT','SWL','PT']
insertFields = ['WELL_ID','TAG','EAST83','NORTH83','UTMZONE','WELL_COMPLETED_DATE','RECEIVED_DATE','FINAL_STATUS_DESCR','USE1','USE2','DEPTH_M','WAT','SWL','PT','RPR','PUMPDUR']
addStuff = arcpy.da.InsertCursor('Wells_Type',insertFields)

with arcpy.da.SearchCursor('Wells_In_Buffer',searchFields) as cursor:
    for row in cursor:
        insertData = list(row)
        insertData.append('')
        insertData.append('')
        print(insertData)
        addStuff.insertRow(insertData)
# except RuntimeError:
#     print('A runtime error has occurred')
