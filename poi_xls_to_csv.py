'''
将Excel格式的POI，转为UTF-8编码的CSV格式
'''

from pathlib import Path
import pandas as pd
from const_variables import poi_xls_folder_filpath, poi_csv_folder_filepath

excel_folder_path = Path(poi_xls_folder_filpath)
csv_folder_path = Path(poi_csv_folder_filepath)

for xls_path in excel_folder_path.glob('**/*.xls'):
    csv_path = (csv_folder_path / xls_path.relative_to(excel_folder_path)).with_suffix('.csv')
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    pd.read_excel(xls_path).to_csv(csv_path, index=False, encoding='UTF-8')
