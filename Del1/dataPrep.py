import arcpy

workspace="D:\\FlemSem3\\Collab\\CollabProj\\CollabProj.gdb"    # do not include these three lines if you bring it into Pro
arcpy.env.workspace = workspace
arcpy.env.overwriteOutput = True

def script_tool(param0,param1,param2,param3,param4):   # master function
  buff = arcpy.analysis.Buffer(param0,param1,param2)
  arcpy.analysis.Intersect([param1,param3],param4)
  return

if __name__ == "__main__":

    param0 = arcpy.GetParameter(0)  # input site
    param1 = arcpy.GetParameterAsText(1)  # output from buffer
    param2 = arcpy.GetParameter(2)  # buffer distance
    param3 = arcpy.GetParameter(3)  # REST
    param4 = arcpy.GetParameterAsText(4)  # intersect output

    script_tool(param0,param1,param2,param3,param4)