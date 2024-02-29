import pandas as pd
import plotly.express as px
import os


class Clean:
    def __init__(self):
        pass

    def load_data(self, path):
        # Import Data and Convert it into a DataFrame
        newpath = os.path.join("data", "raw", path)
        self.data = pd.read_csv(newpath)
        return self.data

    def fill_empty_data(self, data, column, value):
        # Fill empty values with a specific value
        pass

    def scatter_plot(self, data, x, y):
        # Create a scatter plot
        indexed = data.set_index("ID", inplace=True, drop=True)
        fig = px.scatter(
            indexed,
            x=x,
            y=y,
            color="Type",
            title="Price vs Area",
            labels={"Price": "Price (€)", "Habitable Surface": "Area (m²)"},
            hover_data=[
                "Locality",
                "Postal Code",
                "Room Count",
                "Bedroom Count",
                "Bathroom Count",
                "Subtype",
                "Build Year",
            ],
        )
        return self.to_html(fig, f"scatter_plot_{x}_{y}.html")

    def to_html(self, fig, path):
        # Save the plot as an HTML file
        newpath = os.path.join("data", "cleaned", path)
        fig.write_html(newpath)
