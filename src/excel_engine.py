"""
Excel Engine
Handles CSV and Excel files
"""

from pathlib import Path
import pandas as pd


class ExcelEngine:

    def load_file(self, file_path: str):

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"{file_path} not found")

        if path.suffix == ".csv":
            return pd.read_csv(path)

        elif path.suffix in [".xlsx", ".xls"]:
            return pd.read_excel(path)

        else:
            raise ValueError("Unsupported file format")

    def save_excel(self, dataframe, output_path):

        dataframe.to_excel(output_path, index=False)

        print(f"Saved -> {output_path}")