'''
读取arcpy_network生成的成本矩阵表格文件
进行统计、计算、与房屋文件进行链接

geopandas创建的geodataframe占用内存过大
因此，对于OD矩阵的shp文件，不应用它读取。
而是直接读取dbf文件，创建dataframe
'''

import pandas as pd
import numpy as np
from pathlib2 import Path
import traceback
# shp文件使用geopandas
import geopandas
# 生成的OD文件，只读dbf
from simpledbf import Dbf5
import re

from const_variables import (
    od_folder_filepath, od_merge_result_folder_filepath, ked_house_folder_filepath,
    exclude_field_name_list, include_field_name_list, merge_field_name_dict,
    final_field_name_list
)

from slab.logger.base_logger import logger

od_folder_path = Path(od_folder_filepath)
output_folder_path = Path(od_merge_result_folder_filepath)


def get_city_name_from_path(od_table_path: Path) -> str:
    return od_table_path.stem.split('_')[0]


def get_poi_name_from_path(od_table_path: Path) -> str:
    return od_table_path.stem.split('_')[1]


def process_csv():
    pass


def get_city_name_list():
    # 首先获得生成OD矩阵的文件夹中的所有Origin房租城市
    origin_filename_list = []
    for matrix_filepath in Path(od_folder_filepath).glob(f'*_*.csv'):
        matrix_filename = matrix_filepath.stem
        origin_filename, destination_filename = matrix_filename.split('_')
        origin_filename_list.append(origin_filename)
    origin_filename_list = list(set(origin_filename_list))
    return origin_filename_list


def get_od_table_path_list(city_name):
    return list(od_folder_path.glob(f'{city_name}_*.csv'))


def merge_house(house_shp_folder_filepath):
    house_shp_folder_path = Path(house_shp_folder_filepath)

    for origin_filename in get_city_name_list():
        origin_filepath = house_shp_folder_path / (origin_filename + '.shp')
        output_filepath = output_folder_path / origin_filepath.name
        output_filepath = output_filepath.with_suffix('.csv')

        # 如果输出文件存在，则打开已经输出的文件进行追加。否则打开源房租SHP文件
        if output_filepath.exists():
            # origin_df = geopandas.read_file(str())
            origin_df = pd.read_csv(output_filepath)
            print(f'get origin_df from {output_filepath}')
        else:
            origin_df = geopandas.read_file(str(origin_filepath))
            print(f'get origin_df from {origin_filepath}')

        # 不存在元素则跳过
        if origin_df.shape[0] == 0:
            continue

        # 统计城市下，各类POI
        for matrix_filepath in od_folder_path.glob(f'{origin_filename}_*.csv'):
            matrix_filename = matrix_filepath.stem
            _, destination_filename = matrix_filename.split('_')

            # OriginID: 不能使用，内部维护，在Origins图层从1开始
            # Destinat_1: 目的地等级，1为最近的
            # matrix_df[['OriginID', 'Destinatio', 'Destinat_1', 'Total_长']]
            # Name: 源名称 - 目标名称

            # matrix_df = geopandas.read_file(str(matrix_filepath))
            # 不读取shp，读取dbf
            # matrix_dbf = Dbf5(str(matrix_filepath).replace('.shp', '.dbf'))
            # matrix_df = matrix_dbf.to_dataframe()
            # 不读取dbf，读取csv
            matrix_df = pd.read_csv(matrix_filepath)

            # 判断dataframe的元素个数，为0则不进行处理
            if matrix_df.shape[0] == 0:
                continue

            # 根据源名称，重新生成有效的OriginID
            origin_id = [int(name.split(' - ')[0])
                         for name in matrix_df['Name'].values]
            matrix_df.loc[:, 'OriginID'] = origin_id

            # POI计数。先删除重复列
            if (destination_filename + 'Num') in origin_df.columns:
                origin_df = origin_df.drop(columns=destination_filename + 'Num')

            matrix_count_df = matrix_df.loc[:, ['OriginID']]
            try:
                matrix_count_df.loc[:, destination_filename + 'Num'] = 0
            except:
                traceback.print_exc()
                print(matrix_filepath)

            matrix_count_df = matrix_count_df.groupby('OriginID').count()
            origin_df = origin_df.merge(matrix_count_df, 'left',
                                        left_on='ID', right_index=True)

            # POI最短距离。先删除重复列
            if (destination_filename + 'Len') in origin_df.columns:
                origin_df = origin_df.drop(columns=destination_filename + 'Len')

            matrix_len_df = matrix_df.loc[matrix_df['DestinationRank'] == 1, [
                'OriginID', 'Total_长度']]
            matrix_len_df = matrix_len_df.rename(
                columns={'Total_长度': destination_filename + 'Len'})
            matrix_len_df = matrix_len_df.set_index('OriginID')
            origin_df = origin_df.merge(
                matrix_len_df, 'left', left_on='ID', right_index=True)

            origin_df = origin_df.fillna(0)

        # 根据公司分类，计算香浓多样性。公司列CX
        if 'SHDI' in origin_df.columns:
            origin_df = origin_df.drop(columns='SHDI')

        # 公司类别的列
        company_colunm_list = []
        for column in origin_df.columns:
            search_object = re.search(r'C\d+Num', column)
            if search_object is None:
                continue
            company_colunm_list.append(column)

        if len(company_colunm_list) > 0:
            company_sum = origin_df[company_colunm_list].sum(axis=1)
            company_proportion = origin_df[company_colunm_list].divide(company_sum, axis=0)
            company_proportion_log = np.log(company_proportion).replace([np.inf, -np.inf], 0)

            origin_df['SHDI'] = - (company_proportion * company_proportion_log).sum(axis=1)

        # 核密度列名更改
        if 'RASTERVALU' in origin_df.columns:
            origin_df = origin_df.rename(columns={'RASTERVALU': 'KDEValue'})

        # 对字段进行修改
        output_df = field_stat(origin_df, str(output_filepath))

        output_df.to_csv(output_filepath, encoding='utf-8', index=False)


def field_stat(df: pd.DataFrame, filename):
    '''
    修改字段相关信息
    :return:
    '''

    # 错误字段改名
    df = df.rename(columns={
        'ExhibitiNum': 'ExhibitNum', 'ExhibitiLen': 'ExhibitLen',
        'GHoyelNum': 'GHotelNum', 'GHoyelLen': 'GHotelLen',
        'BhstoreNum': 'BHstoreNum', 'BhstoreLen': 'BHstoreLen',
        'TeaHouseNum': 'TeahouseNum', 'TeaHouseLen': 'TeahouseLen',
        'GhosptialNum': 'GhospitalNum', 'GhosptialLen': 'GhospitalLen',
        'AgiculNum': 'AgriculNum', 'AgiculLen': 'AgriculLen'})

    # 统计字段数量
    include_field_count = 0
    exclude_field_count = 0
    for column in df.columns:
        if column in include_field_name_list:
            include_field_count = include_field_count + 1
        if column in exclude_field_name_list:
            exclude_field_count = exclude_field_count + 1

    print(
        f'包括字段：{include_field_count} / {len(include_field_name_list)}，排除字段：{exclude_field_count} / {len(exclude_field_name_list)}')

    # 字段合并，需要在添加缺失字段之前
    for from_field, to_field in merge_field_name_dict.items():
        if (from_field + 'Num') not in df.columns:
            continue

        elif (to_field + 'Num') not in df.columns:
            df[to_field + 'Num'] = df[from_field + 'Num']
            df[to_field + 'Len'] = df[from_field + 'Len']

        else:
            # 数量直接相加
            df[to_field + 'Num'] = df[to_field + 'Num'] + df[from_field + 'Num']

            # 选择最近点数量不为0的行进行最小距离比较
            df_to_min = df.loc[df[from_field + 'Num'] != 0, [from_field + 'Len', to_field + 'Len']]

            # 将被融合字段最短距离为0的赋值为无穷大，从而剔除0可以进行最小值比较
            df_to_min.loc[df_to_min[to_field + 'Len'] == 0, to_field + 'Len'] = np.inf

            # 计算最小值
            df_to_min.loc[:, to_field + 'Len'] = df_to_min[[from_field + 'Len', to_field + 'Len']].min(axis=1)

            # 将结果子集赋值回原始数据帧
            df.loc[df[from_field + 'Num'] != 0, [from_field + 'Len', to_field + 'Len']] = df_to_min

        # 删除被融合的来源列
        df = df.drop(columns=[from_field + 'Num', from_field + 'Len'])

    # 添加缺失的字段

    # for include_field_name in include_field_name_list:
    #     if (include_field_name not in df.columns) and (
    #             include_field_name.rstrip('Num').rstrip('Len') not in list(merge_field_name_dict.keys())
    #     ):
    #         df[include_field_name] = 0
    #         print(f'添加字段：{include_field_name}')

    for final_field_name in final_field_name_list:
        if final_field_name not in df.columns:
            df[final_field_name] = 0
            print(f'添加字段：{final_field_name}')

    # 删除排除的字段
    for exclude_field_name in exclude_field_name_list:
        if exclude_field_name in df.columns:
            df = df.drop(columns=[exclude_field_name])

    # 统计未知字段
    for column in df.columns:
        if (column not in include_field_name_list) and (column not in exclude_field_name_list):
            print(f'未知字段：{column}')
            logger.info(
                f'文件：{filename}，存在未知字段{column}'
            )

    print(f'字段总数：{len(df.columns)}')

    # 字段排序
    df = df[final_field_name_list]

    return df


def clear_dir(dir_path_str):
    for file_path in Path(dir_path_str).glob('*_*.*'):
        file_path.unlink()


if __name__ == "__main__":
    merge_house(ked_house_folder_filepath)
