# Stephen's space for messing around with Python
# WAT

# Some values are blank, some have both | and ;

# There are two values per pipe - a type and a depth. We only need the depth.

# So, when possible, split by pipe, then by semi-colon, then keep the 2nd values.
# From those values, check if they are in ft or m.
# Strip the string characters (' ft' or ' m') and convert to number.
# If it was in feet, convert the number to m. Else, leave it alone.

# Put them back into WAT, delimited by semicolon.

# example_data = ""
example_data = "BRWN ;SAND ;CLAY ;FILL ;0 m;2.43 m|BRWN ;CLAY ;SILT ; DRY ;2.43 m;3.65 m|BRWN ;SAND ;STNS ;WBRG ;3.65 m;4.57 m|"
# example_data = "40 ft"
# example_data = "6 m"

# def ft2m(conv):
#         val = float(conv.group(5))
#         if conv.group(6) == " ft": 
#             val=float(conv.group(5))*0.3048 
#         return str(val)

#import arcpy    # arcpy, so we can turn it into a tool in ArcPro
import re

def colour(geo):
    pipes = geo.split("|")
    semicolon = []
    for x in pipes:
        semicolon = x.split(";")
        return semicolon[0]

# def mat1(geo):
#     data = re.findall('(\s*\w*\s*;)',geo)
#     return data
# def mat2(geo):
#     data = re.findall('(\s*\w*\s*;)',geo)
#     return data
# def mat3(geo):
#     data = re.findall('(\s*\w*\s*;)',geo)
#     return data

# for testing only
print(colour(example_data))
# print(mat1(example_data))
# print(mat2(example_data))
# print(mat3(example_data))
print()