# encoding: utf-8
'''
利用高新公司进行核密度分析生成栅格文件
提取房屋对应的位置的值
'''

import arcpy
from arcpy.sa import *
import os
from os import listdir, makedirs
from os.path import join, basename, splitext, isfile, exists
import glob
import traceback
import pickle

from const_variables import poi_shp_folder_filepath, kde_temp_folder_filepath, ked_house_folder_filepath, \
    house_data_folder_filepath


def input_house(house_shp_folder_filepath):
    for csv_filepath in glob.glob(join(house_shp_folder_filepath, '*.shp')):
        try:
            kde_house(csv_filepath)
        except:
            traceback.print_exc()


def kde_house(house_shp_filepath):
    house_shp_filename = splitext(basename(house_shp_filepath))[0]

    poi_shp_filepath = join(poi_shp_folder_filepath, house_shp_filename, 'AdvanComp.shp')
    output_shp_filepath = join(ked_house_folder_filepath, basename(house_shp_filepath))

    print(house_shp_filepath + ' -> ' + output_shp_filepath)
    if exists(output_shp_filepath):
        print('  exist')
        return

    # 设置环境的范围参数，从而让KDE生产的栅格覆盖整个房租点范围
    arcpy.Describe(house_shp_filepath)
    desc = arcpy.Describe(house_shp_filepath)
    arcpy.env.extent = arcpy.Extent(desc.extent.XMin, desc.extent.YMin, desc.extent.XMax, desc.extent.YMax)

    raster = KernelDensity(poi_shp_filepath, None)
    ExtractValuesToPoints(house_shp_filepath, raster, output_shp_filepath)


if __name__ == "__main__":
    input_house(join(house_data_folder_filepath, 'RentSHP8'))
