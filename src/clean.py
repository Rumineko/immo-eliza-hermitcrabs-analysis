import pandas as pd
import plotly.express as px
import os


class Clean:
    def __init__(self):
        pass

    def load_data(self, path):
        # Import Data and Convert it into a DataFrame
        current_dir = os.path.dirname(os.path.abspath(__file__))
        newpath = os.path.join(current_dir, "..", "data", "raw", path)
        data = pd.read_csv(newpath)
        return data

    def fill_empty_data(self, data, column, value):
        # Fill empty values with a specific value
        pass

    def scatter_plot(self, data, x, y):
        # Create a scatter plot
        indexed = data.set_index("ID", drop=True)

        try:
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
        except ValueError as e:
            print(f"Error: {e}")

    def to_html(self, fig, path):
        # Save the plot as an HTML file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        newpath = os.path.join(current_dir, "..", "data", "cleaned", path)
        fig.write_html(newpath)
