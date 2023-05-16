# This script creates the Borehole_Results table
# and splits the field GEO into it

import arcpy

def script_tool(param0, param1):
    def ft2m(convertMe):
        depthCheck = convertMe.split(" ")
        print(depthCheck)
        if depthCheck[0] == '':
            print(depthCheck[0])
        elif depthCheck[1] == "ft":
            depthCheck[0] = float(depthCheck[0])*0.3048
        return depthCheck[0]

    bhResultsTable = param0
    wellsinbufferTable = param1
    insertFields = ['Well_ID','Colour','Mat1','Mat2','Mat3','Top','Bot']

    # set the relevant fields from the table with the data
    searchFields = ['Well_ID','GEO']
    # create the insert cursor, for populating the new table
    addStuff = arcpy.da.InsertCursor(bhResultsTable, insertFields)
    # create the search cursor, for pulling data from the original table
    pull = arcpy.da.SearchCursor(wellsinbufferTable, searchFields)
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
    print('Process complete.')  # Good job, script!

    return

if __name__ == "__main__":

    param0 = arcpy.GetParameter(0)
    param1 = arcpy.GetParameter(1)

    script_tool(param0, param1)
