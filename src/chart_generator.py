import matplotlib.pyplot as plt


class ChartGenerator:

    def generate_bar_chart(self, dataframe):

        plt.figure(figsize=(8, 5))

        plt.bar(
            dataframe["Product"],
            dataframe["Quantity"]
        )

        plt.title("Sales Quantity by Product")
        plt.xlabel("Product")
        plt.ylabel("Quantity")

        plt.tight_layout()

        plt.savefig("reports/sales_chart.png")

        plt.close()

        print("Chart Generated -> reports/sales_chart.png")