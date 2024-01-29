import pandas as pd


def xlsx_to_csv(xlsx_file_path):
    if xlsx_file_path.endswith('.csv'):
        return xlsx_file_path
    df = pd.read_excel(xlsx_file_path)
    df.to_csv(xlsx_file_path.replace('.xlsx', '.csv'), index=False)

    return xlsx_file_path.replace('.xlsx', '.csv')


