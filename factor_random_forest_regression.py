from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import make_regression

import pandas as pd
from slab.read_util.pandas_read_csv import read_df
from const_variables import job_field_name_list


def test_regression():
    df = read_df('D:\Document\HousePricing\Data\ODMerge\Baoding.csv')
    y = df['RPrice']
    X = df[job_field_name_list]

    regr = RandomForestRegressor()
    regr.fit(X, y)
    R2 = regr.score(X, y)

    print(R2)

if __name__ == '__main__':
    test_regression()


# X, y = make_regression(n_features=4, n_informative=2,
#                        random_state=0, shuffle=False)
# regr = RandomForestRegressor(max_depth=2, random_state=0)
# regr.fit(X, y)
#
# print(regr.predict([[0, 0, 0, 0]]))
