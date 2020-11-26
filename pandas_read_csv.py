from pandas import read_csv, DataFrame


def read_csv_auto_encoding(file_path, recursion=True, **kwargs) -> DataFrame:
    file_path = str(file_path)

    try:
        f = open(file_path, encoding='utf-8')
        try:
            df = read_csv(f, **kwargs)
        except UnicodeDecodeError:
            f.close()
            f = open(file_path, encoding='gbk')
            df = read_csv(f, **kwargs)
        f.close()
    except:
        if recursion:
            return read_csv_auto_encoding(file_path, recursion=False, sep='\t', **kwargs)
        else:
            raise Exception('无法处理的csv文件')

    return df
