import pandas as pd
import os


def export_excel_report(

    df,

    cleaning_report,

    insights,

    output_path="reports/final_report.xlsx"

):

    os.makedirs(
        os.path.dirname(output_path),
        exist_ok=True
    )

    with pd.ExcelWriter(
        output_path,
        engine="openpyxl"
    ) as writer:

        # ===============================
        # Sheet 1
        # ===============================

        df.to_excel(

            writer,

            sheet_name="Cleaned Data",

            index=False

        )

        # ===============================
        # Sheet 2
        # ===============================

        summary = pd.DataFrame({

            "Metric": [

                "Rows",

                "Columns",

                "Missing Values",

                "Duplicate Rows Removed",

                "Empty Rows Removed",

                "Empty Columns Removed"

            ],

            "Value": [

                len(df),

                len(df.columns),

                int(df.isnull().sum().sum()),

                cleaning_report.get(
                    "duplicates_removed",
                    0
                ),

                cleaning_report.get(
                    "empty_rows_removed",
                    0
                ),

                cleaning_report.get(
                    "empty_columns_removed",
                    0
                )

            ]

        })

        summary.to_excel(

            writer,

            sheet_name="Summary",

            index=False

        )

        # ===============================
        # Sheet 3
        # ===============================

        if insights:

            insight_df = pd.DataFrame(

                list(insights.items()),

                columns=[
                    "Insight",
                    "Value"
                ]

            )

            insight_df.to_excel(

                writer,

                sheet_name="AI Insights",

                index=False

            )

        # ===============================
        # Sheet 4
        # ===============================

        stats = df.describe(
            include="all"
        )

        stats.to_excel(

            writer,

            sheet_name="Statistics"

        )

    return output_path