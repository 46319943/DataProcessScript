# -*- coding: utf-8 -*
# from pathlib import Path
from os.path import join

# 城市列表，共105个城市
city_name_list = ['Baoding', 'Baotou', 'Beijing', 'Binzhou', 'Changchun', 'Changji', 'Changsha', 'Changzhou',
                  'Chaoyang', 'Chengdu', 'Chongqing', 'Chuxiong', 'Congzuo', 'Dalian', 'Dandong', 'Dongguan', 'Fuzhou',
                  'Guangzhou', 'Guilin', 'Guiyang', 'Haerbing', 'Haikou', 'Handan', 'Hangzhou', 'Hanzhong', 'Hefei',
                  'Heyuan', 'Heze', 'Huaian', 'Huaihua', 'Huainan', 'Huangshi', 'Huhehaote', 'Huludao', 'Hulunbeier',
                  'Jiamusi', 'Jiaxing', 'Jilin', 'Jinan', 'Kunming', 'Lanzhou', 'Lasa', 'Leshan', 'Liangshan',
                  'Liaoyang', 'Lijiang', 'Linfen', 'Lishui', 'Liuan', 'Liupanshui', 'Loudi', 'Luohe',
                  'Luoyang', 'Luzhou', 'Maanshan', 'Maoming', 'Meizhou', 'Mianyang', 'Mudanjiang', 'Nanchang',
                  'Nanchong', 'Nanjing', 'Nanning', 'Nantong', 'Neijiang', 'Ningbo', 'Panzhihua', 'Qingdao', 'Shanghai',
                  'Shantou', 'Shenyang', 'Shenzhen', 'Shijiazhuang', 'Suqian', 'Suzhou', 'Tacheng', 'Taiyuan',
                  'Tianjin', 'Tianmen', 'Tongren', 'Weifang', 'Weihai', 'Wenshan', 'Wenzhou', 'Wuhan', 'Wuhu',
                  'Wulumuqi', 'Wuwei', 'Wuxi', 'Wuzhong', 'Xiamen', 'Xian', 'Xiantao', 'Xining', 'Yanan', 'Yanbian',
                  'Yangjiang', 'Yangquan', 'Yantai', 'Yichang', 'Yichun', 'Yinchuan', 'Yiyang', 'Zhengzhou', 'Zhuhai']

# POI列表，共45个
poi_name_list = ['BHstore', 'Market', 'Shop', 'Bazaar', 'Fitness', 'Sport', 'Squares', 'Subway', 'Airport', 'Bus',
                 'Railway', 'Cross', 'Coach', 'College', 'Primary', 'Middle', 'GHotel', 'Khotel', 'Xhotel', 'Museum',
                 'Zoo', 'Scenic', 'Park', 'Art', 'Culture', 'Site', 'Exhibit', 'Plant', 'Teahouse', 'Cake', 'Club',
                 'Coffee', 'ForeiEat', 'FastFood', 'ChinaEat', 'Cmine', 'Company', 'Agricul', 'Czone', 'Emerg',
                 'Disease', 'Recuper', 'Clinic', 'SHospital', 'Ghospital']

# 数据目录路径
base_data_folder_filepath = r'C:\Document\HouseData'

# 中国城市行政区目录路径
china_shp_folder_filepath = join(base_data_folder_filepath, 'ChinaSHP')
# POI的Excel文件目录路径
poi_xls_folder_filpath = join(base_data_folder_filepath, 'POI/Excel')
# POI的CSV文件目录路径
poi_csv_folder_filepath = join(base_data_folder_filepath, 'POI/CSV')
# POI的SHP文件目录路径
poi_shp_folder_filepath = join(base_data_folder_filepath, 'POI/SHP')
# 三甲医院的CSV文件路径
a3_hospital_csv_filepath = join(base_data_folder_filepath, '3AHospital.csv')
# 商圈的CSV文件路径
business_district_csv_filepath = join(base_data_folder_filepath, 'BusinessDistrict.csv')
# 全国路网地理数据库gdb文件路径
road_network_geodatabase_filepath = join(base_data_folder_filepath, 'RoadNetwork/roadnet.gdb')
# OD矩阵结果保存目录
od_folder_filepath = join(base_data_folder_filepath, 'ODTable')
# Python3路径
python3_filepath = r'D:\SoftwareInstall\Anaconda\python.exe'
# Python2路径
python2_filepath = r'C:\Python27\ArcGIS10.8\python.exe'
# OD矩阵计算、连接结果保存目录
od_merge_result_folder_filepath = join(base_data_folder_filepath, 'ODMerge')
# OD矩阵计算中，不进行计算的POI名称列表
od_exclude_poi_list = ['Company']
# KDE分析生成的栅格临时文件目录
kde_temp_folder_filepath = join(base_data_folder_filepath, 'KDERaster')
# KDE分析生成的房屋点文件目录
ked_house_folder_filepath = join(base_data_folder_filepath, 'KDEHouse')
# 房屋数据目录路径
house_data_folder_filepath = join(base_data_folder_filepath, 'House')
# 房屋原始数据目录路径
house_origin_data_folder_filepath = join(house_data_folder_filepath, 'Origin')
# 房屋统计目录路径
house_statistics_data_folder_filepath = join(house_data_folder_filepath, 'Statistics')

# 单独的医院POI的SHP文件目录
hospital_poi_shp_folder_filepath = join(base_data_folder_filepath, 'POI/Hospital')


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

poi_hospital_name_list = [
    'Ghospital',
    'SHospital'
]

house_field_name_list = [
    'ID', 'RPrice',
    # 'HPrice',
    'RentWay', 'Area', 'Bedrooms', 'Living_roo', 'Toilet', 'SouthFacin', 'Decorate', 'Floor',
    'Age',
]

community_field_name_list = [
    'Plot_ratio', 'Green_rate', 'Property_f'
]

exclude_field_name_list = [
    'Address', 'Lon84', 'Lat84', 'geometry', 'ratio',
    'ArtNum', 'ArtLen', 'AirportNum', 'AirportLen',
    'C0Num', 'C0Len', 'C1Num', 'C1Len', 'C2Num', 'C2Len', 'C3Num',
    'C3Len', 'C4Num', 'C4Len', 'C5Num', 'C5Len', 'C6Num', 'C6Len',
    'CoffeeNum', 'CoffeeLen', 'CultureNum', 'CultureLen',
    'DiseaseNum', 'DiseaseLen', 'EmergNum', 'EmergLen', 'ExhibitNum', 'ExhibitLen', 'FastFoodNum', 'FastFoodLen',
    'FitnessNum', 'FitnessLen', 'ForeiEatNum', 'ForeiEatLen',
    'GHotelNum', 'GHotelLen',
    'HospitalNum', 'HospitalLen', 'KhotelNum', 'KhotelLen',
    'MuseumNum', 'MuseumLen', 'RecuperNum', 'RecuperLen',
    'TeahouseNum', 'TeahouseLen', 'XhotelNum', 'XhotelLen', 'ZooNum', 'ZooLen',
    'CakeNum', 'CakeLen', 'ChinaEatNum', 'ChinaEatLen',
    'ClinicNum', 'ClinicLen', 'ClubNum', 'ClubLen',
]

job_field_name_list = [
    'KDEValue',
    'AdvanCompNum', 'AdvanCompLen',
    'AgriculNum', 'AgriculLen',
    'CmineNum', 'CmineLen',
    'CzoneNum', 'CzoneLen',
    'SHDI'
]

medical_field_name_list = [
    '3AHospitalNum', '3AHospitalLen', 'GhospitalNum', 'GhospitalLen',
    'SHospitalNum', 'SHospitalLen',
]

convenience_field_name_list = [
    'BazaarNum', 'BazaarLen',
    'BHstoreNum', 'BHstoreLen', 'ShopNum', 'ShopLen',
    'CrossNum', 'CrossLen', 'MarketNum', 'MarketLen',
]

transportation_field_name_list = [
    'BusNum', 'BusLen',
    'CoachNum', 'CoachLen',
    'RailwayNum', 'RailwayLen',
    'SubwayNum', 'SubwayLen',
]

district_field_name_list = [
    'BusinessDistrictNum', 'BusinessDistrictLen'
]

school_field_name_list = [
    'CollegeNum', 'CollegeLen',
    'MiddleNum', 'MiddleLen',
    'PrimaryNum', 'PrimaryLen',

]
landscape_field_name_list = [
    'ParkNum', 'ParkLen',
    'PlantNum', 'PlantLen',
    'SiteNum', 'SiteLen',
    'ScenicNum', 'ScenicLen',
    'SquaresNum', 'SquaresLen',
    'SportNum', 'SportLen',
]

# 将某个字段合并入另一个字段
merge_field_name_dict = {
    'Plant': 'Park',
    'Scenic': 'Site',
    'Shop': 'BHstore',
    'Sport': 'Squares',
}

# 应该包括的字段列表
include_field_name_list = house_field_name_list + community_field_name_list + job_field_name_list \
                          + medical_field_name_list + convenience_field_name_list + transportation_field_name_list \
                          + district_field_name_list + school_field_name_list + landscape_field_name_list

# 融合后的最终字段列表。从包括的字段名列表中，删除融合字段，得到最终的字段
final_field_name_list = include_field_name_list[:]
for merge_field_name in merge_field_name_dict.keys():
    final_field_name_list.remove(merge_field_name + 'Num')
    final_field_name_list.remove(merge_field_name + 'Len')
