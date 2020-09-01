# encoding: utf-8
import arcpy
import os
from os import listdir, makedirs
from os.path import join, basename, splitext, isfile, exists
import glob
import traceback
import pickle

from const_variables import road_network_geodatabase_filepath, poi_shp_folder_filepath, city_name_list, od_folder_filepath

# 覆盖SHP不警告
arcpy.env.overwriteOutput = True

if exists('arcpy_network_result.pkl'):
    with open('arcpy_network_result.pkl', 'rb') as f:
        result_list = pickle.load(f)
else:
    result_list = []


def add_result(output_filepath):
    result_list.append(output_filepath)
    with open('arcpy_network_result.pkl', 'wb') as f:
        pickle.dump(result_list, f)


def build_network():
    '''
    根据路网模板，构建所有城市的路网信息
    当路网源数据或元数据更改后，需要重构路网

    因此此过程只用执行一次，构建完一次路网之后，在不更改相关数据时，不需要重新构建
    '''
    for city_name in city_name_list:
        city_road_network_path = join(road_network_geodatabase_filepath, city_name, city_name + '_ND')
        arcpy.na.BuildNetwork(city_road_network_path)
        print('build network: ' + city_road_network_path)


def input_house_origin(house_folder_filepath):
    for origin_filepath in glob.glob(join(house_folder_filepath, '*.shp')):
        origin_filename = splitext(basename(origin_filepath))[0]

        print(origin_filepath)

        # 是否已经构建OD分析图层
        has_od_layer = False

        network_filepath = join(road_network_geodatabase_filepath, origin_filename, origin_filename + '_ND')

        for destination_filepath in glob.glob(join(poi_shp_folder_filepath, origin_filename, '*.shp')):
            # POI文件名
            destination_filename = splitext(basename(destination_filepath))[0]

            output_filename = origin_filename + '_' + destination_filename + '.csv'
            output_filepath = join(od_folder_filepath,
                                   origin_filename + '_' + destination_filename + '.csv')

            print('   + ' + destination_filepath + ' -> ' + output_filepath)

            if exists(output_filepath):
                print('output file exist')
                continue
            if output_filepath in result_list:
                print('result exist in result list')
                continue

            if not has_od_layer:
                # 创建OD成本矩阵的分析层
                od = arcpy.na.MakeODCostMatrixLayer(
                    network_filepath, origin_filename + 'OD', u'长度', 1200)
                has_od_layer = True
                print('od layer created, adding origin locations')

                # 将房租点添加到OD的Origins子层
                arcpy.na.AddLocations(od, "Origins",
                                      origin_filepath, "Name ID #",
                                      '1200 Meters')
                print('origin added to od layer')

            # 判断当前shp文件中，是否存在要素（存在裁剪之后，要素为空的情况）
            if int(arcpy.GetCount_management(destination_filepath).getOutput(0)) == 0:
                add_result(output_filepath)
                print('null feature in destination')
                continue

            # 将POI点添加到OD的Destinations子层，同时覆盖之前的点
            arcpy.na.AddLocations(od, "Destinations",
                                  destination_filepath, "",
                                  '1200 Meters', append=False)
            try:
                arcpy.na.Solve(od)
            except Exception as e:
                traceback.print_exc()
                # 没找到解
                if 'ERROR 030212' in e.message:
                    add_result(output_filepath)
                    print('no solution')
                    continue
                raise Exception('exception debug')

            # 获取图层组
            odLayerGroup = od.getOutput(0)
            # 按名称生成图层组字典
            subLayers = dict((lyr.datasetName, lyr)
                             for lyr in arcpy.mapping.ListLayers(odLayerGroup)[1:])
            # 获取线状子图层
            lineLayer = subLayers['ODLines']

            # 导出线状图层。只导出属性表为CSV文件
            # arcpy.management.CopyFeatures(lineLayer, output_filepath)
            arcpy.TableToTable_conversion(lineLayer, od_folder_filepath, output_filename)

            execute_script(output_filepath)

            # 记录结果
            add_result(output_filepath)

        # 删除当前房租点生成的OD成本矩阵（其实AddLoc时可以进行Clear，也不用删除）
        if has_od_layer:
            arcpy.Delete_management(od)


def execute_script(output_filepath):
    # 调用脚本处理生成的OD矩阵SHP
    # script_path = r'D:\Document\GeoPython\geopandas\od_matrix_demo.py'
    # python_path = r'python'
    # script_result = os.system(
    #     'activate && ' + python_path + ' ' + script_path)
    # 脚本返回结果不为零说明执行失败
    # if script_result != 0:
    #     print('exec script failed')
    #     continue

    # 处理后，删除shp文件
    # arcpy.Delete_management(output_filepath)

    pass


if __name__ == "__main__":
    # build_network()
    input_house_origin(r'D:\Document\HousePricing\Data\House\RentSHP1')
