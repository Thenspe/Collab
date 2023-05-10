# Stephen's space for messing around with Python
# WAT

# Some values are blank, some have both | and ;

# There are two values per pipe - a type and a depth. We only need the depth.

# So, when possible, split by pipe, then by semi-colon, then keep the 2nd values.
# From those values, check if they are in ft or m.
# Strip the string characters (' ft' or ' m') and convert to number.
# If it was in feet, convert the number to m. Else, leave it alone.

# Put them back into WAT, delimited by semicolon.

#import arcpy    # arcpy, so we can turn it into a tool in ArcPro
import re       # regular expressions for string manipulation

# create a function for the unit conversion of feet to meters
def primary(waterField):
    def stephen_format(matchobj):
        val = float(matchobj.group(2))
        if matchobj.group(3) == "ft": 
            val=float(matchobj.group(2))*0.3048 
        
        return str(val) + " m" 
    waterField = re.sub('(\w+;\s*)(\d+)\s*(ft|m)', stephen_format, waterField)
    return waterField

# example_data = ""
# example_data = "Fresh; 20 ft|"
# example_data = "Fresh; 20 ft|Fresh; 115 ft|"
# print (re.sub('(\w+;\s*)(\d+)\s*(ft|m)', stephen_format, example_data))

# 1st Capturing Group (\w+;\s*)
# \w
#  matches any word character (equivalent to [a-zA-Z0-9_])
# + matches the previous token between one and unlimited times, as many times as possible, giving back as needed (greedy)
# ; matches the character ; with index 5910 (3B16 or 738) literally (case sensitive)
# \s
#  matches any whitespace character (equivalent to [\r\n\t\f\v ])
# * matches the previous token between zero and unlimited times, as many times as possible, giving back as needed (greedy)
# 2nd Capturing Group (\d+)
# \d
#  matches a digit (equivalent to [0-9])
# + matches the previous token between one and unlimited times, as many times as possible, giving back as needed (greedy)
# 3rd Capturing Group (\s*ft)
# \s
#  matches any whitespace character (equivalent to [\r\n\t\f\v ])
# * matches the previous token between zero and unlimited times, as many times as possible, giving back as needed (greedy)
# ft
#  matches the characters ft literally (case sensitive)