import arcpy
import glob
from os.path import join, basename, splitext, isfile, exists, dirname

# Get the layer as a parameter and describe it.
#
# The layer could be a layer in ArcMap (like "some_layer")
# Or, it could be a .lyr file (like "C:/data/some.lyr")
#

for shp_filepath in glob.glob(join('C:/Document/HouseData/House/RentSHP8', '*.shp')):
    # shp_filepath = shp_filepath.replace('\\', '/')

    # ArcGIS10.8的BUG，必须调用两次才能正确识别SHP文件
    desc = arcpy.Describe(shp_filepath)
    desc = arcpy.Describe(shp_filepath)

    print(desc.dataType)


