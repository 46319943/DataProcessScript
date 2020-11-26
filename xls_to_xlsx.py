import pandas as pd
from pathlib import Path
from const_variables import poi_xls_folder_filpath

for xls_path in Path(poi_xls_folder_filpath).glob('**/*.xls'):
    output_path = xls_path.with_suffix('.xlsx')
    print(f'{xls_path} -> {output_path}')

    if output_path.exists():
        print(' exist')
        continue

    df = pd.read_excel(str(xls_path))
    df.to_excel(output_path, index=False)
