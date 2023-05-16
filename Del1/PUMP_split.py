# assumtion: GPM in the MOE database always refers to imperial gallons

# We need only the values from 5, 7, 11 (pump rate, recommended pump rate, pumping duration)
example_data = '8 ft;33 ft;;30 ft;2 GPM;;2 GPM;CLEAR;PUMP;N;1:0;;'
# example_data = ';;;;;;;OTHER;;N;;;'
# example_data = ''
import arcpy
import re

def g2L(conv):
    # this function converts imperial gallons per minute to litres per minute
    if conv.group(2) == 'GPM':
        val = round(float(conv.group(1)*4.546),0)
        return val
    elif conv.group(2) == 'LPM':
        val = conv.group(1)
        return val


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
            print('Before: ',row)
            ptConvert = re.sub('(\d)(\w)',g2L,ptSplit[4]) # check for and make any necessary conversion
            rprConvert = re.sub('(\d)(\w)',g2L,ptSplit[6]) # check for and make any necessary conversion

            row[1] = ptConvert     # assign value from the 5th semicolon to PT
            row[2] = rprConvert     # assign value from the 5th semicolon to RPR
            row[3] = ptSplit[10]    # assign value from the 5th semicolon to PUMPDUR
            # print('After ',row)
            cursor.updateRow(row)


print('Process complete.')