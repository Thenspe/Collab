# Group P2306 Collaborative Project 2023
# Members: Ewan, Kamryn, Stephen
# designed using python 3.0
# Deliverable One

# Deliverable Tasks
    ## 1. Connect to ArcGIS Pro workspace
    ## 2. Buffer Well site, and intersect it with WWIS databse table
    ## 3. Create new fields in intersected site and WWIS table for pipe designation proeprties: Waterfound, diameter, depth
    ## 4. Split client required fields from MOE Wells Report Table by pipe designation
    ## 5. Create and format output report to PDF of required well report fields


# Import necessary modules
import arcpy 
import os
from arcgis.gis import GIS
from arcgis.features import FeatureLayer
import requests
from requests.exceptions import ConnectionError
from time import sleep
import time


# Set gdb workspace 
arcpy.env.workspace = "Y:\Fleming\Collab Project\P2306\P2306.gdb" # Update to your own workspace file path
gdb = arcpy.env.workspace
arcpy.env.overwriteOutput = True
sr = arcpy.SpatialReference(3857) # Set the spatial reference to the standard WGS 1984 Web Mercator (auxiliary sphere) for web layers, using WKID ID

# Set connection to MOE AGS REST ENDPOINT and define variables

# ## Option One ##
# # Use arcpy to make a feature later directly from the hosted feature layer on the REST endpoint,
# # then add it to the gdb for further geo processing

# # Assign a name to the new layer
# layerName = "wellPoints"
# # Rest Endpoint URL
# wellsURL = "https://ws.lioservices.lrc.gov.on.ca/arcgis1071a/rest/services/MOE/Wells/MapServer/0"
# # Create the new feature class
# wellsFC = arcpy.MakeFeatureLayer_management(wellsURL, layerName)
# # Add the new layer to the gdb using feature class to feature classs
# wellsLoc = arcpy.FeatureClassToFeatureClass_conversion(wellsFC, gdb, layerName)

## Option Two ##
# Run a try except to manage if the anything in the REST endpoint has changed

i = 0                   # create an iteration variable for timeout response
wellsLoc = " "          # Create an open string variable, this will be called outside the try except, and only work if the get request works
not_found = True        # add a varaible that evaluates if the url get request is successful
# request response time needs to be less than 30 seconds

while i < 30 and not_found:
    # the try will work to retrieve the URL sucessfully
    try:
        # REST Endpoint URL
        wellsLoc = requests.get("https://ws.lioservices.lrc.gov.on.ca/arcgis1071a/rest/services/MOE/Wells/MapServer/0")
        not_found = False
        # Successful request print statement
        print(" Request verified!")
    # the except will handle any errors, so the code will continue to run
    except ConnectionError:
        # imported sleep function iteration at time varaibles of 1 second
        sleep(1)
        i += 1
        # Print statement for failed request
        print("Request failed")
        break

print(wellsLoc)

# ## Option Three ##
# # Use the argis.features modules to directly make a new feature class within the gdb from the REST Endpoint
# # Rest Endpoint URL
# wellsURL = "https://ws.lioservices.lrc.gov.on.ca/arcgis1071a/rest/services/MOE/Wells/MapServer/0"
# # Assign a name to the new layer
# wellsLoc = "wellPoints"

# # Use arcgis.features modeule to create new feature layer
# fl = FeatureLayer(wellsURL)
# # Query the new feature layer based off of SQL to get all attribtues and properties of the hosted layer
# fs = fl.query()
# # Save the new layer to the gdb
# fs.save(gdb, wellsfc)

# Set workspace for where the construction site files are stored
conSites = "Y:\Fleming\Collab Project\CambiumSampleData"            # Update this to your well sites folder location 
# List the directory the files are located in
for file in os.listdir(conSites):
    # Specify the extension of interest within the directory
    if file.endswith(".shp"):
        # Use OS path to determine the basename of the file, then print
        print("Reading Desired Directory Files...")
        print("...")
        # assign the print function to a varaible 
        n = print(os.path.basename(file).split('.')[0])
        print("Directory Files Printed.")

print(file)

# Site shapefile location
x = "Y:\Fleming\Collab Project\CambiumSampleData\Site\Site.shp" # This is hardcoded temporairly for PoC

# Allow the user to select the site of interest
SoI = input(str("Please enter the site of interest from list above: "))

# Use an if statement to evaluate the input statement
# If true, we create a new feature class of a buffer around the site of interest
if file == SoI:
    # print()
    # print()
    # print("Creating new feature from selected site file.")
    # print("Finishing...")
    # print()
    # # Create a new feature class to store the selected site file in
    # newfc = arcpy.CreateFeatureclass_management(gdb, os.path.basename(file).split('.')[0], "POLYGON", "", "", "", sr)
    fc = arcpy.FeatureClassToGeodatabase_conversion(file, gdb)
    print("New site feature class created and added to gdb!")
    print()
    # Create a string variable for buffer feature class
    newSite = "siteBuffer"
    # Print statements
    print("Buffering Site of Interest...")
    print("Finishing...")
    print("...")
    # Buffer the site
    siteBuf = arcpy.Buffer_analysis(x, newSite, "700 meters")
    print()
    print("Buffer Completed.")
else:
    print()
    end = print("Please select a site in the Water Well Sites database. Would you like to select again (y/n) ?")
    print()
    if end == 'n':
        print()


# We need to clip the well site locations to the buffer zone
# Using the connections to the server directly, we can clip the shapefile to our gdb

# First create a string variable for buffer clip feature class
wellSites = "wellClip"

# This will provide us with the subset of the records and wells that we need.
# Now we can clip the wells to the site buffer                        
Wells = arcpy.Clip_analysis(wellsLoc, siteBuf, wellSites)

# # now that our site is buffered, and wells of interest are clipped to that buffer,
# # we can intersect the report table to the study area
# wellSoI = arcpy.Intersect_analysis([Wells, serverURL], "WoI")







# fld1 = arcpy.AddField_management(tbl, "WellID", "TEXT")
# fld2 = arcpy.AddField_management(tbl, "GEO1", "TEXT")
# fld3 = arcpy.AddField_management(tbl, "GEO2", "TEXT")
# fld4 = arcpy.AddField_management(tbl, "GEO3", "TEXT")
# fld5 = arcpy.AddField_management(tbl, "GEO4", "TEXT")
# fld6 = arcpy.AddField_management(tbl, "GEO5", "TEXT")
# fld7 = arcpy.AddField_management(tbl, "GEO6", "TEXT")



# # Define the parameters for the UpdateCursor() function to iterate through the feature class 
# # to split the string value based on a delimiter and remove leading and trailing blank spaces in the new fields.
# with arcpy.da.UpdateCursor(tbl, ["GEO", "GEO1", "GEO2", "GEO3", "GEO4", "GEO5", "GEO6"]) as cursor:
    
#     for row in cursor:
#         entries = len(row[0].split("|"))
#     x = 0

#     while x != entries:
#         row[x+1]=row[0].split("|")[x]
#         x+1
       
#         row=[i.strip() if i is not None else None for i in row]
#         cursor.updateRow(row)
