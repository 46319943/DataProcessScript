'''
目前只考虑了租房数据

对房屋数据进行过滤：
1.去除重复数据，基于经纬度坐标、房租和面积去重;
2.去除房租0.2%的最大值和最小值，即保留中间99.6%的值；
3.面积area范围：10-150平方米，其他去除；
4.数据中的Null值先全部补为0；
5.计算房租/面积，去除0.2%的最大值和最小值，保留中间99.6%的值

房屋的原始数据放在House/Origin下
输出在House下

如：
House/Origin/RentCSV1
->
House/RentCSV1

'''

from statistics_func import filter
from pathlib import Path
import pandas as pd
from const_variables import house_origin_data_folder_filepath, house_data_folder_filepath, house_statistics_data_folder_filepath
from slab.read_util.pandas_read_csv import read_df


def house_filter(house_csv_folder_filepath, price_field='RPrice'):
    '''
    根据房屋原始数据目录进行过滤、统计

    :param house_csv_folder_filepath: 包含CSV文件的目录

    '''
    house_csv_folder_path = Path(house_csv_folder_filepath)
    house_data_folder_path = Path(house_data_folder_filepath)

    df_statistics = pd.DataFrame(columns=['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max'])

    for csv_path in house_csv_folder_path.glob('*.csv'):
        print(f'{csv_path} ->')

        df = read_df(csv_path)
        df = filter(df, price_field=price_field)
        output_path = house_data_folder_path / house_csv_folder_path.stem / csv_path.relative_to(house_csv_folder_path)
        output_path.parent.mkdir(exist_ok=True)
        df.to_csv(output_path, index=False, encoding='UTF-8')

        print(f'    {output_path}')

        # 进行统计
        statistics_series = df[price_field].describe()

        statistics_series.name = csv_path.stem
        df_statistics = df_statistics.append(statistics_series)

    df_statistics.index.name = 'city'
    return df_statistics


def house_origin_filter():
    '''
    对原始数据目录下的所有数据进行处理
    '''
    for house_csv_folder_path in Path(house_origin_data_folder_filepath).glob('*Rent*'):
        df_statistics = house_filter(house_csv_folder_path)
        df_statistics.to_csv(
            (Path(house_statistics_data_folder_filepath) / house_csv_folder_path.stem).with_suffix('.csv'),
            encoding='UTF-8'
        )
    for house_csv_folder_path in Path(house_origin_data_folder_filepath).glob('*Resold*'):
        df_statistics = house_filter(house_csv_folder_path, price_field='HPrice')
        df_statistics.to_csv(
            (Path(house_statistics_data_folder_filepath) / house_csv_folder_path.stem).with_suffix('.csv'),
            encoding='UTF-8'
        )


if __name__ == "__main__":
    house_origin_filter()
