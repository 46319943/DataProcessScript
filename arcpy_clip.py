# -*- coding: utf-8 -*

'''
根据城市行政区边界进行裁剪，输出SHP
Python2代码
'''

import os
from os import listdir, makedirs
from os.path import join, basename, splitext, isfile, exists, dirname
import glob
import arcpy
import xlrd

from const_variables import city_name_list, china_shp_folder_filepath, poi_csv_folder_filepath, poi_shp_folder_filepath, a3_hospital_csv_filepath, business_district_csv_filepath, get_city_district_shp_filepath

# 创建WGS84坐标系对象
spatial_ref = arcpy.SpatialReference(4326)


def clip_poi():
    '''
    对POI目录下的CSV文件进行裁剪，输出到SHP对应目录
    同时，对商圈、三甲医院也进行裁剪
    '''
    for city_name in city_name_list:
        city_csv_folder_filepath = join(poi_csv_folder_filepath, city_name)
        city_shp_folder_filepath = join(poi_shp_folder_filepath, city_name)
        for csv_filepath in glob.glob(join(city_csv_folder_filepath, '*.csv')):
            clip_csv(
                csv_filepath, city_shp_folder_filepath, x_field='经度_wgs84', y_field='纬度_wgs84'
            )
        city_district_shp_filepath = get_city_district_shp_filepath(city_name)
        clip_csv(a3_hospital_csv_filepath, city_shp_folder_filepath,
                 x_field='longitude_wgs84', y_field='latitude_wgs84',
                 district_shp_filepath=city_district_shp_filepath)
        clip_csv(business_district_csv_filepath, city_shp_folder_filepath,
                 x_field='longitude_wgs84', y_field='latitude_wgs84',
                 district_shp_filepath=city_district_shp_filepath)


def clip_house(house_csv_folder_filepath):
    '''
    对指定房屋CSV目录中的文件进行裁剪，输出到对应SHP目录
    '''
    house_shp_folder_filepath = house_csv_folder_filepath.replace('CSV', 'SHP')
    for csv_filepath in glob.glob(join(house_csv_folder_filepath, '*.csv')):
        clip_csv(
            csv_filepath, house_shp_folder_filepath
        )
    pass


def clip_multi_house(house_folder_filepath):
    '''
    寻找指定文件下，包含房屋的CSV目录，并遍历裁剪
    '''
    for house_shp_folder_filepath in glob.glob(join(house_folder_filepath, '*CSV*')):
        clip_house(house_shp_folder_filepath)


def clip_csv(csv_filepath, shp_folder_filepath, district_shp_filepath=None, x_field='Lon84', y_field='Lat84', override=False):
    '''
    输入CSV文件路径，根据行政区划进行裁切，输出到指定目录

    :param csv_filepath: CSV文件路径
    :param shp_folder_filepath: 生成SHP的输出目录路径。文件名会根据输入的CSV文件路径确定
    :param district_shp_filepath: 用于裁剪的行政区划SHP文件路径。不填写会根据CSV文件路径中包含的城市名称自动推断
    :param x_field: CSV文件的经度字段
    :param y_field: CSV文件的纬度字段
    :param override: SHP的输出文件路径存在时，是否覆盖。默认跳过
    '''
    # 文件名，不带后缀
    csv_filename = splitext(basename(csv_filepath))[0]

    # 生成SHP文件的路径，创建父目录
    output_shp_filepath = join(shp_folder_filepath, csv_filename + '.shp')
    if not exists(shp_folder_filepath):
        makedirs(shp_folder_filepath)

    # 输出路径
    print(csv_filepath + ' -> ' + output_shp_filepath)

    # 没提供行政区划SHP文件路径，则根据中国行政区划目录与CSV文件路径自动生成
    if district_shp_filepath is None:
        # 判断文件名是否为城市
        if csv_filename in city_name_list:
            district_shp_filepath = get_city_district_shp_filepath(csv_filename)
        # 判断父目录名是否为城市
        else:
            csv_parent_folder_name = basename(dirname(csv_filepath))
            if csv_parent_folder_name in city_name_list:
                district_shp_filepath = get_city_district_shp_filepath(csv_parent_folder_name)
            else:
                raise Exception('district shapefile filepath error')

    if exists(output_shp_filepath):
        if not override:
            print('exist and skip')
            return
        else:
            print('exist and override')

    arcpy.MakeXYEventLayer_management(
        csv_filepath, x_field, y_field, csv_filename + 'Event', spatial_ref)

    arcpy.Delete_management(output_shp_filepath)

    arcpy.Clip_analysis(
        csv_filename + 'Event', district_shp_filepath, output_shp_filepath)

    arcpy.Delete_management(csv_filename + 'Event')

    return


if __name__ == "__main__":
    clip_poi()
    # clip_house(r'D:\Document\HousePricing\Data\House\RentCSV1')
    # clip_multi_house(r'D:\Document\HousePricing\Data\House')
