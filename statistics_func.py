import pandas as pd
from numpy import nan
ERROR_VALUE = -1


def filter(df: pd.DataFrame, price_field='RPrice') -> pd.DataFrame:
    df = df.copy()
    df = df.dropna()

    # 处理有问题的RPrice和Area
    df[price_field] = df[price_field].apply(to_float)
    error_series = (df[price_field] == ERROR_VALUE).value_counts()
    if True in error_series.index:
        error_count = (df[price_field] == ERROR_VALUE).value_counts()[True]
        print(f'{price_field} error count: {error_count}')
        df[price_field] = df[price_field][df[price_field] != ERROR_VALUE]

    df['Area'] = df['Area'].apply(to_float)
    error_series = (df['Area'] == ERROR_VALUE).value_counts()
    if True in error_series.index:
        error_count = (df['Area'] == ERROR_VALUE).value_counts()[True]
        print(f'Area error count: {error_count}')
        df['Area'] = df['Area'][df['Area'] != ERROR_VALUE]

    # 处理之后，异常值被设为na，去除
    df = df.dropna()

    # 去重复
    df = df.drop_duplicates([price_field, 'Area', 'Lon84', 'Lat84'])

    # 选取99.6%房租
    price_min, price_max = df[price_field].quantile(
        0.002), df[price_field].quantile(1-0.002)
    df = df[(df[price_field] > price_min) & (df[price_field] < price_max)]

    # 选取面积
    df = df[(df['Area'] > 10) & (df['Area'] < 150)]

    # df = df[df['RentWay'] != 1]

    # 计算 房租 / 面积，并选取99.6%
    df['ratio'] = df[price_field] / df['Area']
    ratio_min, ratio_max = df['ratio'].quantile(
        0.002), df['ratio'].quantile(1-0.002)
    df = df[(df['ratio'] > ratio_min) & (df['ratio'] < ratio_max)]

    # 用房租价格，删除outliers
    price_q1, price_q3 = df[price_field].quantile(
        0.25), df[price_field].quantile(0.75)
    price_iqr = price_q3 - price_q1
    price_bottom_bound = price_q1 - 1.5 * price_iqr
    price_top_bound = price_q3 + 1.5 * price_iqr
    df = df[(df[price_field] > price_bottom_bound)
            & (df[price_field] < price_top_bound)]

    return df


def process(df: pd.DataFrame, name: str, price_field='RPrice') -> pd.Series:
    df = filter(df)

    statistics_series = df[price_field].describe()
    statistics_series.name = name

    return statistics_series


def to_float(value, error_value=-1):
    try:
        return float(value)
    except:
        return ERROR_VALUE
