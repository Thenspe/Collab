# WAT

# Some values are blank, some have both | and ;

# There are two values per pipe - a type and a depth. We only need the depth.

# So, when possible, split by pipe, then by semi-colon, then keep the 2nd values.
# From those values, check if they are in ft or m.
# Strip the string characters (' ft' or ' m') and convert to number.
# If it was in feet, convert the number to m. Else, leave it alone.

# Put them back into WAT, delimited by semicolon.

# example_data = ""
# example_data = ";1.52 m|;2.57 m|"
# example_data = "Fresh; 20 ft|"
# example_data = "Fresh; 20 ft|Fresh; 115 ft|"
# print (re.sub('(\w+;\s*)(\d+)\s*(ft|m)', stephen_format, example_data))

import re       # regular expressions for string manipulation

# create a function for the unit conversion of feet to meters
def primary(waterField):            # function required for ArcGIS Pro code block
    def stephen_format(matchobj):   # function for unit conversion
        val = float(matchobj[1])    # convers value from string to number
        if matchobj[2] == "ft":     # checks for ft vs m
            val=round((float(matchobj[1])*0.3048),2)    # converts ft to m, rounds to 2 decimals
        return str(val) + " m"      # returns the number plus the new unit
    
    waterField = re.findall('(\w*;\s*)([\d\.]+)\s*(ft|m)', waterField)  # regex to isolate string, explanation below
    waterReturn = str()             # creates a blank string variable
    for m in waterField:            # iterates through each section of the string in the field
        waterReturn += stephen_format(m) + "; " # function  call for unit conversion
        print(waterReturn)          # not required for code block, just for testing
    return waterReturn              # return number value to code block

# everything above this goes in the code block
primary(example_data)
print()



# 1st Capturing Group (\w*;\s*)
# \w
#  matches any word character (equivalent to [a-zA-Z0-9_])
# * matches the previous token between zero and unlimited times, as many times as possible, giving back as needed (greedy)
# ; matches the character ; with index 5910 (3B16 or 738) literally (case sensitive)
# \s
#  matches any whitespace character (equivalent to [\r\n\t\f\v ])
# * matches the previous token between zero and unlimited times, as many times as possible, giving back as needed (greedy)
# 2nd Capturing Group ([\d\.]+)
# Match a single character present in the list below [\d\.]
# + matches the previous token between one and unlimited times, as many times as possible, giving back as needed (greedy)
# \d matches a digit (equivalent to [0-9])
# \. matches the character . with index 4610 (2E16 or 568) literally (case sensitive)
# \s
#  matches any whitespace character (equivalent to [\r\n\t\f\v ])
# * matches the previous token between zero and unlimited times, as many times as possible, giving back as needed (greedy)
# 3rd Capturing Group (ft|m)
# 1st Alternative ft
# ft
#  matches the characters ft literally (case sensitive)
# 2nd Alternative m
# m matches the character m with index 10910 (6D16 or 1558) literally (case sensitive)