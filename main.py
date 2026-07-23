from src.excel_engine import ExcelEngine
from src.data_cleaner import DataCleaner
from src.excel_formatter import ExcelFormatter
from src.chart_generator import ChartGenerator

engine = ExcelEngine()
cleaner = DataCleaner()
formatter = ExcelFormatter()
chart = ChartGenerator()

df = engine.load_file("data/sales_data.csv")

print("\nOriginal Data\n")

print(df)

df = cleaner.clean_data(df)

engine.save_excel(df, "output/cleaned_sales.xlsx")

formatter.format_excel("output/cleaned_sales.xlsx")

chart.generate_bar_chart(df)

print(df)

print("\nProject Completed Successfully")