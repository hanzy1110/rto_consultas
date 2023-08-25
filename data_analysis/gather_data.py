import os
from numpy import empty
import pandas as pd
import pathlib

DATASET = pathlib.Path(os.getcwd()) / "dataset"
print(DATASET)

def get_data_by_year(year, folder_path):

    dataframes = []
    dirpath, dirname, filenames = next(os.walk(folder_path))
    for filename in filenames:
        print(filename)
        file_path = os.path.join(folder_path, filename)
        df = pd.read_csv(file_path, dtype={"Dominiovehiculo": str})
        # Read each CSV file and append it to the list
        if len(df.columns) != 7:
            print(df)
            continue
        elif filename[:4] != str(year):
            print(filename)
            continue
        dataframes.append(df)

    if dataframes:
        print(len(dataframes))
        return pd.concat(dataframes, ignore_index=True)
    else:
        return pd.DataFrame()

for year in range(2015, 2023):
    df = get_data_by_year(year, DATASET)
    if not df.empty:
        df.to_csv(DATASET / f"joined/{year}_CERTIFICADOS.csv")
