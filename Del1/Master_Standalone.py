"""
This script was created by Stephen VanDam for the Fleming College Collaborative Project 2306 in May of 2023. 

It takes an input from the Ministry of the Environment Well Water Information System REST endpoint, after a buffer and
intersect to reduce the number of wells, and outputs 3 tables, populated and with units converted from imperial to metric. 
"""

import arcpy
import re
import os
from datetime import date

workspace="D:\\FlemSem3\\Collab\\CollabProj\\CollabProj.gdb"    # do not include these three lines if you bring it into Pro
arcpy.env.workspace = workspace
arcpy.env.overwriteOutput = True

def script_tool(param0,param1,param2):   # master function

    dataTable = param0 # 'Wells_In_Buffer'
    tables = ['Wells_Type','Borehole_Results','Borehole_Details']
    tableFields = [     # Set the field names for the tables
            #well_type  1       2       3           4                5                  6                  7           8       9     10       11    12    13   14       15
            ['WELL_ID','TAG','EAST83','NORTH83','UTMZONE','WELL_COMPLETED_DATE','RECEIVED_DATE','FINAL_STATUS_DESCR','USE1','USE2','DEPTH_M','WAT','SWL','PT','RPR','PUMPDUR'],
            # borehole_results      3     4      5      6    7
            ['WELL_ID','Colour','Mat1','Mat2','Mat3','Top','Bot'],
            # borehole_details     3        4       5       6       7       8       9         10       11       12
            ['WELL_ID','HOLE_D','HOLE_T','HOLE_B','CAS_M','CAS_D','CAS_T','CAS_B','SCRN_D','SCRN_M','SCRN_T','SCRN_B']
        ]
    tableAlias = [      # Set the alias for the tables
            # well_type
            ['Well ID','TAG','Easting','Northing','UTM Zone','Well Completion Date','Received Date','Final Status','Use 1','Use 2','Well Depth','Water First Found','Static Water Level','PT','Recommended Pump Rate','Pump Duration'],
            # borehole_results
            ['Well ID','Colour','Material 1','Material 2','Material 3','Upper limit','Lower limit'],
            # borehole_details
            ['Well ID','Hole Diameter (cm)','Hole Top','Hole Bottom','Casing Material','Casing Casing Diameter (cm)','Casing Top','Casing Bottom','Screen Diameter (cm)','Screen Material','Screen Top','Screen Bottom']
        ]
    stratigraphy = 'GEO'
    MOE_Holes = ['HOLE','CAS','SCRN']
    outTables = []
    today = str(date.today())
    
    # set output table file path and name;
    for x in range(len(tables)):
        csvTable = os.path.join(param1,today + ' - ' +param2 + ' - ' + tables[x] + '.csv')
        outTables.append(csvTable)
        print(outTables[x])

    def addSomeFields(table,field,alias):
    # Step 2 - This function iterates through adding fields to some tables
        x = 0
        while x < len(field):
            fieldLength = 20
            if field[x] == tableFields[0][7] or field[x] == tableFields[0][8] or field[x] == tableFields[0][9] or field[x] == tableFields[0][11] or field[x] == tableFields[0][13]:
                fieldLength = 100
            else:
                fieldLength = 20
            arcpy.management.AddField(table,field[x],'TEXT',field_length=fieldLength,field_alias=alias[x],field_is_nullable=True)
            x+=1

    def ft2m(convertMe):
    # Step 3B, Step 4D - this functions converts units in ft to m AND from inches to cm
        if convertMe.group(2) == 'ft':
            val = round(float(convertMe.group(1))*0.3048,2) # converts feet to metres
        elif convertMe.group(2) == 'inch':
            val = round(float(convertMe.group(1))*2.54,2) # converts inches to centimetres
        else:
            val = convertMe.group(1)
        return str(val)
    
    def equalLengths(checklist,value,blanks):
    # Step 3 C - this function adds empty fields to match list lengths
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
    
    def g2L(conv):
    # Step 4C - this function converts imperial gallons per minute to litres per minute
        if conv.group(2) == 'GPM':
            val = round(float(conv.group(1))*4.546,0) # convert to float and multiply
            return str(val)     # convert back to string for the return
        elif conv.group(2) == 'LPM':
            val = conv.group(1)
            return val
        else:
            raise Exception("PT Unit is in neither GPM nor LPM.",conv.group(1),conv.group(2),row)
        
    ####################################################################################

    # Step 2 - Name and create the three tables
    t = 0
    while t < len(tables):
        if arcpy.Exists(tables[t]):         # check if the tables already exist. Delete them if they do.
            print("Table",tables[t],"exists, deleting . . .")
            arcpy.Delete_management(tables[t])
            print("Table",tables[t],"deleted.")
        print("Creating table",tables[t],". . .")
        arcpy.management.CreateTable(arcpy.env.workspace,tables[t])   # Create new tables
        print("Table",tables[t],"created.")
        print()

        addSomeFields(tables[t],tableFields[t],tableAlias[t])   # Run the add fields function
        t+=1    # iterate

    print('Step 2: Create Tables - COMPLETE.')

####################################################################################

    # Step 3 - Populate the tables

    # - # - # - # - # - # - # - # - #

    # Step 3 A - tables[0] Wells_Type
    searchFields = [tableFields[0][:-2]]
    insertFields = [tableFields[0]]
    addStuff = arcpy.da.InsertCursor(tables[0],insertFields)

    with arcpy.da.SearchCursor(dataTable,searchFields) as cursor:
        for row in cursor:
            insertData = list(row)  # convert row into a list
            insertData.append('')   # add two blank entries (for RPR and PUMPDUR)
            insertData.append('')
            # print(insertData)
            addStuff.insertRow(insertData)  # populate the table
    del addStuff    # close the insert cursor

    # - # - # - # - # - # - # - # - #

    # Step 3 B - tables[1] Borehole_Results
    insertFields = [tableFields[1]]

    # set the relevant fields from the table with the data
    searchFields = [tableFields[0][0],stratigraphy]
    # create the insert cursor, for populating the new table
    addStuff = arcpy.da.InsertCursor(tables[1], insertFields)
    # create the search cursor, for pulling data from the original table
    pull = arcpy.da.SearchCursor(dataTable, searchFields)
    for row in pull:                # for each row in the original table...
        # print("pull:",pull)
        pipes = pull[1].split("|")  # separate by the pipes.
        # print("pipes:",pipes)
        for x in pipes:             # for each set of pipes...
            semicolons = x.split(";")   # separate by the semicolons.
            # print(pull[0])
            # print(len(semicolons))
            if len(semicolons) > 1:     # only add lines that have values in them
                addStuff.insertRow([pull[0],semicolons[0],semicolons[1],semicolons[2],semicolons[3],re.sub('([\d\.]+)\s*(\w+)',ft2m,semicolons[4]),re.sub('([\d\.]+)\s*(\w+)',ft2m,semicolons[5])])

                # print(semicolons)
    del pull        # close the cursors to prevent errors
    del addStuff
    # print('Process complete.')  # Good job, script!

    # - # - # - # - # - # - # - # - #

    # Step 3 C - tables[2] Borehole Details

    searchFor = [tableFields[0][0],MOE_Holes[0],MOE_Holes[1],MOE_Holes[2]] # fields to pull from
    putItHere = [tableFields[2]]   # fields to place data into
    inCursor = arcpy.da.InsertCursor(tables[2],putItHere)             # prep the insert cursor

    with arcpy.da.SearchCursor(dataTable,searchFor) as cursor:    # create the search cursor to pull data
        for row in cursor:                      # for each row
            # print(row)
            holeSplit = row[1].split('|')    # split the data from the HOLE column
            casSplit = row[2].split('|')      # split the data from the CAS column
            scrnSplit = row[3].split('|')     # split the data from the SCRN column

            # Discover longest number of pipes
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
        del inCursor # close the cursor
    print('Step 3: Populate tables - COMPLETE.')
    
    ####################################################################################
    
    # Step 4 - Unit Conversions

    # Step 4 A - WAT - Calculate Field

    arcpy.management.CalculateField(in_table=tables[0], field=tableFields[0][11], expression=("primary(!"+tableFields[0][11]+"!)"), code_block="""import re
def primary(waterField):            # function required for ArcGIS Pro code block
    def WATft2m(matchobj):          # function for unit conversion
        val = float(matchobj[1])    # converts value from string to number
        if matchobj[2] == "ft":     # checks for ft vs m
            val=round((float(matchobj[1])*0.3048),2)    # converts ft to m, rounds to 2 decimals
        return str(val) + " m"      # returns the number plus the new unit
    
    waterField = re.findall('(\w*;\s*)([\d\.]+)\s*(ft|m)', waterField)  # regex to isolate string
    waterReturn = str()             # creates a blank string variable
    for m in waterField:            # iterates through each section of the string in the field
        waterReturn += WATft2m(m) + "; " # function  call for unit conversion
    return waterReturn              # return number value to code block
""")

    # Step 4 B - Static Water Level - Calculate Field
    swlSearch = tableFields[0][12]
    with arcpy.da.UpdateCursor(tables[0],swlSearch) as cursor:
        for row in cursor:
            for each in range(len(row)):
                converted = re.sub('([\d\.]+)\s*(\w+)',ft2m,row[each])
                row[each] = converted
            cursor.updateRow(row)


    # Part 4 C - Pumping info - Populate and Convert
    ptSearch = [tableFields[0][0],tableFields[0][13],tableFields[0][14],tableFields[0][15]] #fields to reference and update
    with arcpy.da.UpdateCursor(tables[0], ptSearch) as cursor:  # create the update cursor
        for row in cursor:
            # print('Row:',row)
            # print(len(row[1]))
            if len(row[1]) > 1:                 # if PT is not empty
                ptSplit = row[1].split(';')     # split PT by semicolon
                # print(ptSplit[4] + '|' + ptSplit[6] + '|' + ptSplit[10])
                # print('Before: ',ptSplit)
                ptConvert = re.sub('([\d\.]+)\s*(\w+)',g2L,ptSplit[4]) # check for and make any necessary conversion
                rprConvert = re.sub('([\d\.]+)\s*(\w+)',g2L,ptSplit[6]) # check for and make any necessary conversion

                row[1] = ptConvert    # assign value from the 5th semicolon to PT
                row[2] = rprConvert     # assign value from the 5th semicolon to RPR
                row[3] = ptSplit[10]    # assign value from the 5th semicolon to PUMPDUR
                cursor.updateRow(row)
    
    # Part 4 D - Borehole_Results - Convert
    bhrSearch = [tableFields[2][1:]] #fields to reference and update
    with arcpy.da.UpdateCursor(tables[2], bhrSearch) as cursor:  # create the update cursor
        for row in cursor:
            for each in range(len(row)):    # divides the row by field
                field = re.sub('([\d\.]+)\s*(\w+)',ft2m,row[each]) # for each field, call the function for unit conversion
                row[each] = field   # replaces the row value with the converted unit
            cursor.updateRow(row)

    print('Step 4: Unit Conversions - COMPLETE.')

    ####################################################################################
    # Step 5 - .csv outputs
    
    for t in range(len(tables)):
        arcpy.conversion.ExportTable(tables[t],outTables[t],sort_field=tableFields[t][0],use_field_alias_as_name=True)
        print("Table",t,"export complete.")
    print('Step 5: Table Exports - COMPLETE.')
    
    return

if __name__ == "__main__":

    # param0 = arcpy.GetParameter(0) # Wells_In_Buffer
    # param0 = 'CambiumPeterboroug_Intersect'
    param0 = 'Fleming_Intersect'
    param1 = 'D:/FlemSem3/Collab/P2306/Del1/Outputs' # output folder
    param2 = '1234' # project number

    script_tool(param0,param1,param2)
