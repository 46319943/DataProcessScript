# -*- coding: utf-8 -*
# from pathlib import Path
from os.path import join

# 城市列表，共105个城市
city_name_list = ['Baoding', 'Baotou', 'Beijing', 'Binzhou', 'Changchun', 'Changji', 'Changsha', 'Changzhou', 'Chaoyang', 'Chengdu', 'Chongqing', 'Chuxiong', 'Congzuo', 'Dalian', 'Dandong', 'Dongguan', 'Fuzhou', 'Guangzhou', 'Guilin', 'Guiyang', 'Haerbing', 'Haikou', 'Handan', 'Hangzhou', 'Hanzhong', 'Hefei', 'Heyuan', 'Heze', 'Huaian', 'Huaihua', 'Huainan', 'Huangshi', 'Huhehaote', 'Huludao', 'Hulunbeier', 'Jiamusi', 'Jiaxing', 'Jilin', 'Jinan', 'Kunming', 'Lanzhou', 'Lasa', 'Leshan', 'Liangshan', 'Liaoyang', 'Lijiang', 'Linfen', 'Lishui', 'Liuan', 'Liupanshui', 'Loudi', 'Luohe',
                  'Luoyang', 'Luzhou', 'Maanshan', 'Maoming', 'Meizhou', 'Mianyang', 'Mudanjiang', 'Nanchang', 'Nanchong', 'Nanjing', 'Nanning', 'Nantong', 'Neijiang', 'Ningbo', 'Panzhihua', 'Qingdao', 'Shanghai', 'Shantou', 'Shenyang', 'Shenzhen', 'Shijiazhuang', 'Suqian', 'Suzhou', 'Tacheng', 'Taiyuan', 'Tianjin', 'Tianmen', 'Tongren', 'Weifang', 'Weihai', 'Wenshan', 'Wenzhou', 'Wuhan', 'Wuhu', 'Wulumuqi', 'Wuwei', 'Wuxi', 'Wuzhong', 'Xiamen', 'Xian', 'Xiantao', 'Xining', 'Yanan', 'Yanbian', 'Yangjiang', 'Yangquan', 'Yantai', 'Yichang', 'Yichun', 'Yinchuan', 'Yiyang', 'Zhengzhou', 'Zhuhai']

# 中国城市行政区目录路径
china_shp_folder_filepath = r'D:\Document\HousePricing\Data\ChinaSHP'
# POI的Excel文件目录路径
poi_xls_folder_filpath = r'D:\Document\HousePricing\Data\POI\Excel'
# POI的CSV文件目录路径
poi_csv_folder_filepath = r'D:\Document\HousePricing\Data\POI\CSV'
# POI的SHP文件目录路径
poi_shp_folder_filepath = r'D:\Document\HousePricing\Data\POI\SHP'
# 三甲医院的CSV文件路径
a3_hospital_csv_filepath = r'D:\Document\HousePricing\Data\3AHospital.csv'
# 商圈的CSV文件路径
business_district_csv_filepath = r'D:\Document\HousePricing\Data\BusinessDistrict.csv'
# 全国路网地理数据库gdb文件路径
road_network_geodatabase_filepath = r'D:\Document\HousePricing\Data\RoadNetwork\roadnet.gdb'
# OD矩阵结果保存目录
od_folder_filepath = r'D:\Document\HousePricing\Data\ODTable'
# Python3路径
python3_filepath = r'D:\SoftwareInstall\Anaconda\python.exe'
# Python2路径
python2_filepath = r'C:\Python27\ArcGIS10.8\python.exe'
# OD矩阵计算、连接结果保存目录
od_merge_result_folder_filepath = r'D:\Document\HousePricing\Data\ODMerge'
# KDE分析生成的栅格临时文件目录
kde_temp_folder_filepath = r'D:\Document\HousePricing\Data\KDERaster'
# KDE分析生成的房屋点文件目录
ked_house_folder_filepath = r'D:\Document\HousePricing\Data\KDEHouse'


def get_city_district_shp_filepath(city_name):
    '''
    根据城市名称，获取城市对应的行政区划SHP文件路径
    '''
    if city_name not in city_name_list:
        raise Exception('invalid city name')
    return join(china_shp_folder_filepath, city_name + '.shp')


advance_company_pattern_list = [
    r'电子',
    r'信息.*技',
    r'生物',
    r'航天',
    r'航空',
    r'新材料',
    r'金属.*材料',
    r'高分子.*材料',
    r'能源',
    r'资源.*环境',
    r'环境.*资源',
    r'自动化'
]

advance_zone_pattern_list = [
    r'信息',
    r'电子',
    r'生物',
    r'医药',
    r'材料',
    r'能源',
    r'电子'
]

classify_pattern_list = [
    r'信息',
    r'电子',
    r'生物',
    r'医药',
    r'材料',
    r'能源',
]