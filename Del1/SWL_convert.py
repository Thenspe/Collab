# Stephen's space for messing around with Python
# WAT

# Some values are blank, some have both | and ;

# There are two values per pipe - a type and a depth. We only need the depth.

# So, when possible, split by pipe, then by semi-colon, then keep the 2nd values.
# From those values, check if they are in ft or m.
# Strip the string characters (' ft' or ' m') and convert to number.
# If it was in feet, convert the number to m. Else, leave it alone.

# Put them back into WAT, delimited by semicolon.

import arcpy
import re

workspace="D:\\FlemSem3\\Collab\\CollabProj\\CollabProj.gdb"    # do not include these three lines if you bring it into Pro
arcpy.env.workspace = workspace
arcpy.env.overwriteOutput = True

example_data = '45 m'

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

print(statWater(example_data))