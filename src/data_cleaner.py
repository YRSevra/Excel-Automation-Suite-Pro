import pandas as pd


class DataCleaner:

    def clean_data(self, df):

        original_rows = len(df)

        # Remove duplicate rows
        df = df.drop_duplicates()

        # Remove completely empty rows
        df = df.dropna(how="all")

        # Fill missing values
        df = df.fillna("N/A")

        # Remove extra spaces
        df.columns = [col.strip() for col in df.columns]

        text_columns = df.select_dtypes(include="object").columns

        for col in text_columns:
            df[col] = df[col].str.strip()

        print("\n========== CLEANING REPORT ==========")
        print(f"Original Rows : {original_rows}")
        print(f"Final Rows    : {len(df)}")
        print("Duplicates Removed Successfully")
        print("Missing Values Filled")
        print("Column Names Standardized")
        print("=====================================\n")

        return df