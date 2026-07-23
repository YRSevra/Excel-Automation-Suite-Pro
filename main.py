from src.excel_engine import ExcelEngine
from src.data_cleaner import DataCleaner
from src.excel_formatter import ExcelFormatter

engine = ExcelEngine()
cleaner = DataCleaner()

df = engine.load_file("data/sales_data.csv")

print("\nOriginal Data\n")

print(df)

df = cleaner.clean_data(df)

engine.save_excel(df, "output/cleaned_sales.xlsx")

print(df)

print("\nProject Completed Successfully")