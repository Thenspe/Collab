"""
Script documentation
This tool creates three tables for data output. It populates them from a given input
(wells within a buffer area) and splits and converts the data as required.

It is assumed that GPM is Imperial Gallons per Minute, not US Gallons Per Minute.
On final output, all units are in meters unless otherwise specified.
"""
import arcpy
import re


def script_tool(param0):   # master function

    def addSomeFields(table,field,alias):
    # Step 2 - This function iterates through adding fields to some tables
        x = 0
        while x < len(field):
            fieldLength = 20
            if field[x] == 'FINAL_STATUS_DESCR' or field[x] == 'USE1' or field[x] == 'USE2' or field[x] == 'WAT' or field[x] == 'PT':
                fieldLength = 100
            else:
                fieldLength = 20
            arcpy.management.AddField(table,field[x],'TEXT',field_length=fieldLength,field_alias=alias[x],field_is_nullable=True)
            x+=1

    def ft2m(convertMe):
        depthCheck = convertMe.split(" ")
        # print(depthCheck)
        if depthCheck[0] == '':
            print(depthCheck[0]) # required for IF statement to run
        elif depthCheck[1] == "ft":
            depthCheck[0] = float(depthCheck[0])*0.3048
        return depthCheck[0]
    
    def equalLengths(checklist,value,blanks):
    # step 3 C - this function  does something useful
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
            raise Exception("PT Unit is in neither GPM nor LPM.")
    
    dataTable = param0 # 'Wells_In_Buffer'
    # Step 2 - Name and create the three tables
    tables = ['Wells_Type','Borehole_Results','Borehole_Details']
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

        tableFields = [     # Set the field names for the tables
            #well_type
            ['WELL_ID','TAG','EAST83','NORTH83','UTMZONE','WELL_COMPLETED_DATE','RECEIVED_DATE','FINAL_STATUS_DESCR','USE1','USE2','DEPTH_M','WAT','SWL','PT','RPR','PUMPDUR'],
            # borehole_results
            ['WELL_ID','Colour','Mat1','Mat2','Mat3','Top','Bot'],
            # borehole_details
            ['WELL_ID','HOLE_D','HOLE_T','HOLE_B','CAS_M','CAS_D','CAS_T','CAS_B','SCRN_D','SCRN_M','SCRN_T','SCRN_B']
        ]
        tableAlias = [      # Set the alias for the tables
            # well_type
            ['Well ID','TAG','Easting','Northing','UTM Zone','Well Completion Date','Received Date','Final Status','Use 1','Use 2','Well Depth','Water First Found','Static Water Level','PT','Recommended Pump Rate','Pump Duration'],
            # borehole_results
            ['Well ID','Colour','Material 1','Material 2','Material 3','Upper limit','Lower limit'],
            # borehole_details
            ['Well ID','Hole Diameter','Hole Top','Hole Bottom','Casing Material','Casing Casing Diameter','Casing Top','Casing Bottom','Screen Diameter','Screen Material','Screen Top','Screen Bottom']
        ]

        addSomeFields(tables[t],tableFields[t],tableAlias[t])   # Run the add fields function
        t+=1    # iterate

    print('Step 2: Create Tables - COMPLETE.')

############################################################################################################################

    # Step 3 - Populate the tables

    # - # - # - # - # - # - # - # - #

    # Step 3 - A - tables[0] Wells_Type

    searchFields = ['WELL_ID','TAG','EAST83','NORTH83','UTMZONE','WELL_COMPLETED_DATE','RECEIVED_DATE','FINAL_STATUS_DESCR','USE1','USE2','DEPTH_M','WAT','SWL','PT']
    insertFields = ['WELL_ID','TAG','EAST83','NORTH83','UTMZONE','WELL_COMPLETED_DATE','RECEIVED_DATE','FINAL_STATUS_DESCR','USE1','USE2','DEPTH_M','WAT','SWL','PT','RPR','PUMPDUR']
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
    insertFields = ['Well_ID','Colour','Mat1','Mat2','Mat3','Top','Bot']

    # set the relevant fields from the table with the data
    searchFields = ['Well_ID','GEO']
    # create the insert cursor, for populating the new table
    addStuff = arcpy.da.InsertCursor(tables[1], insertFields)
    # create the search cursor, for pulling data from the original table
    pull = arcpy.da.SearchCursor(dataTable, searchFields)
    for row in pull:                # for each row in the original table...
        # print(pull)
        pipes = pull[1].split("|")  # separate by the pipes.
        # print(pipes)
        for x in pipes:             # for each set of pipes...
            semicolons = x.split(";")   # separate by the semicolons.
            # print(pull[0])
            # print(len(semicolons))
            if len(semicolons) > 1:     # only add lines that have values in them
                addStuff.insertRow([pull[0],semicolons[0],semicolons[1],semicolons[2],semicolons[3],ft2m(semicolons[4]),ft2m(semicolons[5])])

                # print(semicolons)
    del pull        # close the cursors to prevent errors
    del addStuff
    # print('Process complete.')  # Good job, script!

    # - # - # - # - # - # - # - # - #

    # Step 3 C - tables[2] Borehole Details

    searchFor = ['WELL_ID','HOLE','CAS','SCRN'] # fields to pull from
    putItHere = ['WELL_ID','HOLE_D','HOLE_T','HOLE_B','CAS_M','CAS_D','CAS_T','CAS_B','SCRN_D','SCRN_M','SCRN_T','SCRN_B']   # fields to place data into
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
                    # print([row[0],*semiH,*semiC,*semiS])
                    raise Exception('whoops')
        del inCursor # close the cursor
    print('Step 3: Populate tables - COMPLETE.')
    
    ############################################################################################################################
    
    # Step 4 - Well_Type Unit Conversions

    # Step 4 A - WAT - Calculate Field

    arcpy.management.CalculateField(in_table=tables[0], field="WAT", expression="primary(!WAT!)", code_block="""import re
def primary(waterField):            # function required for ArcGIS Pro code block
    def WATft2m(matchobj):   # function for unit conversion
        val = float(matchobj[1])    # convers value from string to number
        if matchobj[2] == "ft":     # checks for ft vs m
            val=round((float(matchobj[1])*0.3048),2)    # converts ft to m, rounds to 2 decimals
        return str(val) + " m"      # returns the number plus the new unit
    
    waterField = re.findall('(\w*;\s*)([\d\.]+)\s*(ft|m)', waterField)  # regex to isolate string, explanation below
    waterReturn = str()             # creates a blank string variable
    for m in waterField:            # iterates through each section of the string in the field
        waterReturn += WATft2m(m) + "; " # function  call for unit conversion
    return waterReturn              # return number value to code block
""")

    # Step 4 B - Static Water Level - Calculate Field
    arcpy.management.CalculateField(in_table=tables[0], field="SWL", expression="primary(!SWL!)", code_block="""import re
def statWater(waterField):
    def ft2m(conv):
        val = float(conv.group(1))
        if conv.group(2) == " ft": 
            val=round((float(conv.group(1))*0.3048),1)
            return str(val)
        elif conv.group(2) == " m":
            val = round(val,1)
            return str(val)
    converted = re.sub('([\d\.]+)(\s*\w+)',ft2m,waterField)
    return converted
""")

    # Part 4 C - Pumping info - Populate and Convert
    ptSearch = ['WELL_ID','PT','RPR','PUMPDUR'] #fields to reference and update
    with arcpy.da.UpdateCursor(tables[0], ptSearch) as cursor:  # create the update cursor
        for row in cursor:
            # print('Row:',row)
            # print(len(row[1]))
            if len(row[1]) > 1:                 # if PT is not empty
                ptSplit = row[1].split(';')     # split PT by semicolon
                # print(ptSplit[4] + '|' + ptSplit[6] + '|' + ptSplit[10])
                # print('Before: ',ptSplit)
                ptConvert = re.sub('(\d*)\s*(\w+)',g2L,ptSplit[4]) # check for and make any necessary conversion
                rprConvert = re.sub('(\d*)\s*(\w+)',g2L,ptSplit[6]) # check for and make any necessary conversion

                row[1] = ptConvert    # assign value from the 5th semicolon to PT
                row[2] = rprConvert     # assign value from the 5th semicolon to RPR
                row[3] = ptSplit[10]    # assign value from the 5th semicolon to PUMPDUR
                cursor.updateRow(row)

    print('Step 4: Well_Type Unit Conversions - COMPLETE.')
    return

if __name__ == "__main__":

    param0 = arcpy.GetParameter(0) # Wells_In_Buffer

    script_tool(param0)