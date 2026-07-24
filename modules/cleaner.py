import pandas as pd


def clean_dataframe(df):

    report = {}

    # Original Shape
    report["original_rows"] = len(df)
    report["original_columns"] = len(df.columns)

    # Remove Empty Rows
    empty_rows = df.isnull().all(axis=1).sum()
    df = df.dropna(how="all")

    # Remove Empty Columns
    empty_columns = df.isnull().all().sum()
    df = df.dropna(axis=1, how="all")

    # Remove Duplicate Rows
    duplicate_rows = df.duplicated().sum()
    df = df.drop_duplicates()

    # Strip Column Names
    df.columns = df.columns.str.strip()

    # Strip Text Values
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype(str).str.strip()

    # Missing Values
    missing_values = int(df.isnull().sum().sum())

    report["empty_rows_removed"] = int(empty_rows)
    report["empty_columns_removed"] = int(empty_columns)
    report["duplicates_removed"] = int(duplicate_rows)
    report["missing_values"] = missing_values

    report["final_rows"] = len(df)
    report["final_columns"] = len(df.columns)

    return df, report