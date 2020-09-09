'''
根据三甲医院列表，将各个城市中的三甲医院从医院中删除
将专科医院和综合医院的结果合并为普通医院，存入Hospital.csv
'''

from pathlib import Path
import pandas as pd
from const_variables import a3_hospital_csv_filepath, poi_csv_folder_filepath, city_name_list, poi_hospital_name_list
from slab.read_util.pandas_read_csv import read_df
import re


def classify_hospital():
    # 读取全国三甲医院列表，获取医院名称
    df_a3 = pd.read_csv(a3_hospital_csv_filepath)
    a3_hospital_name_list = df_a3['name'].values

    poi_csv_folder_path = Path(poi_csv_folder_filepath)
    for city_name in city_name_list:

        # 专科医院与综合医院合并，得到去除三甲医院之后的普通医院
        df_hospital_total = pd.DataFrame()
        poi_hospital_output_path = poi_csv_folder_path / city_name / 'Hospital.csv'

        print(f'{poi_hospital_output_path}   <- ')

        for poi_hospital_name in poi_hospital_name_list:

            poi_hospital_csv_path = poi_csv_folder_path / city_name / poi_hospital_name
            poi_hospital_csv_path = poi_hospital_csv_path.with_suffix('.csv')

            print(f'   + {poi_hospital_csv_path}')

            df_poi_hospital = pd.read_csv(poi_hospital_csv_path)
            hospital_name_list = df_poi_hospital['名称'].values

            for index, hospital_name in enumerate(hospital_name_list):
                # 对于是三甲医院的名称，赋值为空，对DataFrame去除空行
                if is_a3_hospital(hospital_name, a3_hospital_name_list):
                    hospital_name_list[index] = None

            df_poi_hospital['名称'] = hospital_name_list
            df_poi_hospital = df_poi_hospital.dropna()

            df_hospital_total = df_hospital_total.append(df_poi_hospital)

        df_hospital_total.to_csv(poi_hospital_output_path, index=False, encoding='UTF-8')


def is_a3_hospital(hospital_name, a3_hospital_name_list):
    for a3_hospital_name in a3_hospital_name_list:
        if is_same_hospital(a3_hospital_name, hospital_name):
            return True
    return False


def is_same_hospital(a3_hospital_name: str, hospital_name: str):
    '''
    根据名称，判断两所医院是否是同一所医院
    '''

    # 候选名列表
    a3_hospital_alternative_list = []

    # 使用符号分割，得到候选词列表
    a3_hospital_name = re.sub(r'[）)]', '', a3_hospital_name)
    a3_hospital_alternative_list = re.split(r'[\(（、]', a3_hospital_name)

    for a3_hospital_alternative_name in a3_hospital_alternative_list:
        if a3_hospital_alternative_name in hospital_name:
            return True
        elif hospital_name in a3_hospital_alternative_name:
            return True
    return False


if __name__ == "__main__":
    classify_hospital()
