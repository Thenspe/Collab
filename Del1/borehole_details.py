# Stephen's space for messing around with Python

import arcpy

def equalLengths(checklist,value,blanks):
    if checklist[-1].find(';') == -1:
        checklist.pop()
    # print(checklist)
    while len(checklist) < value:
        if blanks == 3:
            checklist.append(';;')
        else:
            checklist.append(';;;')
    # print(checklist)
    return checklist

workspace="D:\\FlemSem3\\Collab\\CollabProj\\CollabProj.gdb"
arcpy.env.workspace = workspace

searchTable = 'Wells_In_Buffer'             # table to pull data from
inTable = 'Borehole_Details'                # table to put data in
searchFor = ['WELL_ID','HOLE','CAS','SCRN'] # fields to pull from
putItHere = ['WELL_ID','HOLE_D','HOLE_T','HOLE_B','CAS_M','CAS_D','CAS_T','CAS_B','SCRN_D','SCRN_M','SCRN_T','SCRN_B']   # fields to place data into
inCursor = arcpy.da.InsertCursor(inTable,putItHere)             # prep the insert cursor

with arcpy.da.SearchCursor(searchTable,searchFor) as cursor:    # create the search cursor to pull data
    for row in cursor:                      # for each row
        # print(row)
        holeSplit = row[1].split('|')    # split the data from the HOLE column
        casSplit = row[2].split('|')      # split the data from the CAS column
        scrnSplit = row[3].split('|')     # split the data from the SCRN column

        #Discover longest number of pipes
        longest = max(len(holeSplit),len(casSplit),len(scrnSplit))
        lenAdjH = equalLengths(holeSplit,longest,3)
        lenAdjC = equalLengths(casSplit,longest,4)
        lenAdjS = equalLengths(scrnSplit,longest,4)
        # print("First split complete.")

        for x in range((longest-1)):
            # For each pipe, split by semicolon and insert row
            semiH = lenAdjH[x].split(';')
            semiC = lenAdjC[x].split(';')
            semiS = lenAdjS[x].split(';')
            # print("Second split complete.")

            # print('final:',[row[0],*semiH,*semiC,*semiS])
            # print(len([row[0],*semiH,*semiC,*semiS]))

            try:
                inCursor.insertRow([row[0],*semiH,*semiC,*semiS])
            except(TypeError):
                print([row[0],*semiH,*semiC,*semiS])
                raise Exception('whoops')


print('Process complete.')