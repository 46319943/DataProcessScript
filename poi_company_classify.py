'''
根据名称对公司、园区进行分类
1、高新技术相关的公司、园区，合并公司园区，成为一类AdvanComp
2、将公司分为多个类别，从而后续计算香浓多样性指数
'''

from pathlib import Path
from re import sub
from const_variables import poi_csv_folder_filepath, city_name_list, advance_company_pattern_list, advance_zone_pattern_list, classify_pattern_list
import pandas as pd
import numpy as np
import re
import traceback
from typing import List


def process_advance():
    '''
    根据POI的CSV目录下各城市的Compay、Czone，提取
    '''
    csv_folder_path = Path(poi_csv_folder_filepath)
    for city_name in city_name_list:
        try:
            city_folder_path = csv_folder_path / city_name
            company_path = city_folder_path / 'Company.csv'
            czone_path = city_folder_path / 'Czone.csv'
            advance_path = city_folder_path / 'AdvanComp.csv'
            print(f'{company_path} + {czone_path} -> {advance_path}')

            df_company = filter_advance_company(pd.read_csv(company_path))
            df_zone = filter_advance_zone(pd.read_csv(czone_path))
            df_advance = df_company.append(df_zone)
            df_advance.to_csv(advance_path, index=False)
        except:
            traceback.print_exc()


def filter_with_pattern_list_function(pattern_list):
    def filter_wrapper_function(name):
        name = str(name)
        for pattern in pattern_list:
            if re.search(pattern, name) is not None:
                return name
        return None
    return filter_wrapper_function


def filter_advance_company(df: pd.DataFrame) -> pd.DataFrame:
    df = df[df['二类'] == '公司企业;公司']

    df['名称'] = df['名称'].apply(filter_with_pattern_list_function(advance_company_pattern_list))
    df = df.dropna(subset=['名称'])

    return df


def filter_advance_zone(df: pd.DataFrame) -> pd.DataFrame:
    df = df[df['二类'] == '公司企业;园区']

    df['名称'] = df['名称'].apply(filter_with_pattern_list_function(advance_zone_pattern_list))
    df = df.dropna(subset=['名称'])

    return df


def process_classify():
    csv_folder_path = Path(poi_csv_folder_filepath)
    for city_name in city_name_list:
        try:
            city_folder_path = csv_folder_path / city_name
            company_path = city_folder_path / 'Company.csv'
            czone_path = city_folder_path / 'Czone.csv'

            df_company = pd.read_csv(company_path)
            df_zone = pd.read_csv(czone_path)
            df = df_company.append(df_zone)

            print(f'{company_path} + {czone_path}')

            for name, sub_df in classify_dataframe_apply(df):
                output_temp_path = city_folder_path / f'C{name}.csv'
                sub_df.to_csv(output_temp_path)
                print(f'    -> {output_temp_path}')

        except:
            traceback.print_exc()


def classify_dataframe_apply(df: pd.DataFrame) -> List[pd.DataFrame]:
    '''
    在Apply函数中，循环操作Series速度很慢
    填raw参数，从而传入ndarray，加快速度

    在Apply操作前，预先定义生成列
    否则，返回ndarray长度不一致时，报错
    '''

    df['name_type'] = 0
    df['name_pattern'] = ''

    def classify_function_series(series: pd.Series):
        name = str(series['名称'])
        for index, classify_pattern in enumerate(classify_pattern_list):
            if re.search(classify_pattern, name) is not None:
                series['name_type'] = index
                series['name_pattern'] = classify_pattern
                return series
        series['name_type'] = index + 1
        series['name_pattern'] = ''
        return series

    def classify_function_raw(series: np.ndarray):
        name = str(series[0])
        for index, classify_pattern in enumerate(classify_pattern_list):
            if re.search(classify_pattern, name) is not None:
                series[-2:] = [index, classify_pattern]
                return series
        series[-2:] = [index + 1, '']
        return series

    df = df.apply(classify_function_raw, axis=1, raw=True)
    return [(name, sub_df) for name, sub_df in df.groupby('name_type')]


def classify_dataframe_plain(df: pd.DataFrame) -> List[pd.DataFrame]:

    name_list = df['名称'].values
    name_type_list = list()
    name_pattern_list = list()

    for name in name_list:
        name = str(name)
        has_match = False
        for index, classify_pattern in enumerate(classify_pattern_list):
            if re.search(classify_pattern, name) is not None:
                name_type_list.append(index)
                name_pattern_list.append(classify_pattern)
                has_match = True
                break

        if not has_match:
            name_type_list.append(index + 1)
            name_pattern_list.append('')

    df['name_type'] = name_type_list
    df['name_pattern'] = name_pattern_list
    return [(name, sub_df) for name, sub_df in df.groupby('name_type')]


if __name__ == "__main__":
    process_advance()
    process_classify()
