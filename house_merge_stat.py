'''
统计计算结果
'''

from pathlib import Path
from const_variables import city_name_list, od_merge_result_folder_filepath, poi_shp_folder_filepath, poi_name_list
from slab.logger.base_logger import stream_file_logger

import os
import shutil

logger = stream_file_logger(os.path.basename(__file__))


def poi_stat():
    '''
    POI统计

    :return:
    '''
    poi_shp_folder_path = Path(poi_shp_folder_filepath)
    for city_name in city_name_list:
        poi_path_list = list((poi_shp_folder_path / city_name).glob('*.shp'))
        poi_list = [poi_path.stem for poi_path in poi_path_list]
        for poi_name in poi_name_list:
            if poi_name not in poi_list:
                logger.info(f'城市：{city_name}，POI：{poi_name}，缺失')


def poi_rename():
    '''
    POI重命名

    :return:
    '''
    rename_dict = {
        'Exhibiti': 'Exhibit',
        'GHoyel': 'GHotel',
        'Bhstore': 'BHstore',
        'TeaHouse': 'Teahouse',
        'Ghosptial': 'Ghospital',
        'Agicul': 'Agricul'
    }

    poi_shp_folder_path = Path(poi_shp_folder_filepath)
    for city_name in city_name_list:
        for from_name, to_name in rename_dict.items():
            for path_to_rename in (poi_shp_folder_path / city_name).glob(f'{from_name}.*'):
                path_new = path_to_rename.with_name(to_name + path_to_rename.suffix)
                path_to_rename.replace(path_new)
                logger.info(f'{path_to_rename} -> {path_new}')


def miss_stat():
    '''
    统计缺失城市
    :return:
    '''

    od_merge_result_folder_path = Path(od_merge_result_folder_filepath)
    od_merge_result_csv_list = list(od_merge_result_folder_path.glob('*.csv'))
    od_merge_city_name_list = [od_merge_result_csv.stem for od_merge_result_csv in od_merge_result_csv_list]
    for city_name in city_name_list:
        if city_name not in od_merge_city_name_list:
            logger.info(f'{city_name} miss')


if __name__ == '__main__':
    poi_rename()
