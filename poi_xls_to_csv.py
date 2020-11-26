'''
将Excel格式的POI，转为UTF-8编码的CSV格式
同时，对于首列列名错误的，进行修改1
'''

from pathlib import Path
import pandas as pd
from const_variables import poi_xls_folder_filpath, poi_csv_folder_filepath

excel_folder_path = Path(poi_xls_folder_filpath)
csv_folder_path = Path(poi_csv_folder_filepath)

for xls_path in excel_folder_path.glob('**/*.xlsx'):
    csv_path = (csv_folder_path / xls_path.relative_to(excel_folder_path)).with_suffix('.csv')
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    df = pd.read_excel(xls_path)
    if str(df.columns[0]) == '1':
        df = df.rename(columns={df.columns[0]: '名称'})
        print(f'fix first column for {csv_path}')
    df.to_csv(csv_path, index=False, encoding='UTF-8')
