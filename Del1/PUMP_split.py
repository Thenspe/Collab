# Stephen's space for messing around with Python

# We need only the values from 5, 7, 11 (pump rate, recommended pump rate, pumping duration)
example_data = '8 ft;33 ft;;30 ft;2 GPM;;2 GPM;CLEAR;PUMP;N;1:0;;'
# example_data = ';;;;;;;OTHER;;N;;;'
# example_data = ''
import arcpy

workspace="D:\\FlemSem3\\Collab\\CollabProj\\CollabProj.gdb"
arcpy.env.workspace = workspace

table = 'Wells_Type' # table to update
ptSearch = ['WELL_ID','PT','RPR','PUMPDUR'] #fields to reference and update

with arcpy.da.UpdateCursor(table, ptSearch) as cursor:  # create the update cursor
    for row in cursor:
        # print(row)
        # print(len(row[1]))
        if len(row[1]) > 1:                 # if PT is not empty
            ptSplit = row[1].split(';')     # split PT by semicolon
            # print(ptSplit[4] + '|' + ptSplit[6] + '|' + ptSplit[10])
            # print('Before: ',row)
            row[1] = ptSplit[4]     # assign value from the 5th semicolon to PT
            row[2] = ptSplit[6]     # assign value from the 5th semicolon to RPR
            row[3] = ptSplit[10]    # assign value from the 5th semicolon to PUMPDUR
            # print('After ',row)
            # this is where you'd work the conversion process in
            cursor.updateRow(row)



# bufferedTable = 'Wells_In_Buffer'
# typeTable = 'Well_Type'
# # check if the table already exists, remove it if it does.
# if arcpy.Exists(typeTable):
#     print(typeTable + ' table exists, deleting...')
#     arcpy.Delete_management(typeTable)
#     print('Table deleted.')
# print("Creating table.")

# # create the table
# arcpy.management.CreateTable(workspace,typeTable)
# # set the fields for the new table
# insertFields = ['WELL_ID','TAG','EAST83','NORTH83','UTMZONE','WELL_COMPLETED_DATE','RECEIVED_DATE','FINAL_STATUS_DESCR','USE1','USE2','DEPTH_M','WAT','SWL','PT']
# # add fields to the table
# for x in insertFields:
#     arcpy.management.AddField(typeTable,x,'TEXT')


print('Process complete.')