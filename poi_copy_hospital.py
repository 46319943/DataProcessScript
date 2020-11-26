'''
将POI中的医院单独拷贝出到一个文件
'''

from const_variables import poi_shp_folder_filepath, city_name_list, hospital_poi_shp_folder_filepath
from pathlib import Path
import shutil

poi_shp_folder_path = Path(poi_shp_folder_filepath)
hospital_poi_shp_folder_path = Path(hospital_poi_shp_folder_filepath)

for city_name in city_name_list:
    print(city_name + ' : ')

    city_folder_path = poi_shp_folder_path / city_name
    dest_city_folder_path = hospital_poi_shp_folder_path / city_name
    dest_city_folder_path.mkdir(exist_ok=True)

    for hospital_path in city_folder_path.glob('3AHospital.*'):
        print(f'  -> {hospital_path}')
        shutil.copy(hospital_path, dest_city_folder_path)

    for hospital_path in city_folder_path.glob('Hospital.*'):
        print(f'  -> {hospital_path}')
        shutil.copy(hospital_path, dest_city_folder_path)
