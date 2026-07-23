from fpdf import FPDF
from datetime import datetime
import os


class PDFExporter:

    def create_pdf(self, dataframe):

        os.makedirs("reports", exist_ok=True)

        pdf = FPDF()
        pdf.add_page()

        pdf.set_font("Arial", "B", 18)
        pdf.cell(190, 10, "Sales Report", ln=True, align="C")

        pdf.ln(5)

        pdf.set_font("Arial", "", 12)

        pdf.cell(190, 8, f"Generated: {datetime.now().strftime('%d-%m-%Y %H:%M')}", ln=True)

        pdf.cell(190, 8, f"Total Records: {len(dataframe)}", ln=True)

        pdf.ln(5)

        total_sales = (dataframe["Quantity"] * dataframe["Price"]).sum()

        pdf.cell(190, 8, f"Total Sales: Rs. {total_sales}", ln=True)

        pdf.ln(10)

        if os.path.exists("reports/sales_chart.png"):
            pdf.image("reports/sales_chart.png", w=170)

        pdf.output("reports/sales_report.pdf")

        print("PDF Report Generated -> reports/sales_report.pdf")