import pandas as pd


def generate_insights(df, value_column, category_column):

    insights = {}

    if value_column:

        insights["max"] = df[value_column].max()

        insights["min"] = df[value_column].min()

        insights["mean"] = round(
            df[value_column].mean(),
            2
        )

        insights["sum"] = round(
            df[value_column].sum(),
            2
        )

    else:

        insights["max"] = None
        insights["min"] = None
        insights["mean"] = None
        insights["sum"] = None

    if category_column:

        insights["top_category"] = (
            df[category_column]
            .value_counts()
            .idxmax()
        )

    else:

        insights["top_category"] = "N/A"

    insights["rows"] = len(df)

    insights["missing"] = int(
        df.isnull().sum().sum()
    )

    insights["duplicates"] = int(
        df.duplicated().sum()
    )

    return insights