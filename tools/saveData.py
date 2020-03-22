import pandas as pd


def save(arr, f, sheet_name):
    if len(arr):
        df = pd.DataFrame(arr, columns=arr[0].keys())
        print(df.head())
        df.to_excel(f, sheet_name=sheet_name, index=False)
