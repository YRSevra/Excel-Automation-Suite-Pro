import pandas as pd


def advanced_analysis(df):

    numeric = df.select_dtypes(include="number")

    if numeric.empty:
        return None

    return {
        "describe": numeric.describe().T,
        "correlation": numeric.corr()
    }