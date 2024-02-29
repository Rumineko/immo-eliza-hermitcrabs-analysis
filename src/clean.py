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
        indexed = data.set_index("ID", drop=True)
        return indexed

    def fill_empty_data(self, data, column, value):
        # Fill empty values with a specific value
        pass

    def append_data(self, data):
        # Append new data to the existing data
        current_dir = os.path.dirname(os.path.abspath(__file__))
        postals = pd.read_csv(os.path.join(current_dir, "zipcodes.csv"))
        for postalcode in data["Postal Code"]:
            municipality = postals[postals["Postcode"] == postalcode]["Hoofdgemeente"]
            province = postals[postals["Postcode"] == postalcode]["Provincie"]
            if not municipality.empty:
                data.loc[data["Postal Code"] == postalcode, "Municipality"] = (
                    municipality.values[0]
                )
            if not province.empty:
                data.loc[data["Postal Code"] == postalcode, "Province"] = (
                    province.values[0]
                )
        with open(
            os.path.join(current_dir, "..", "data", "cleaned", "appended_data.csv"),
            "w",
            encoding="utf-8",
        ) as f:
            data.to_csv(f)

    def load_appended_data(self, path):
        # Import Data and Convert it into a DataFrame
        current_dir = os.path.dirname(os.path.abspath(__file__))
        newpath = os.path.join(current_dir, "..", "data", "cleaned", path)
        data = pd.read_csv(newpath)
        indexed = data.set_index("ID", drop=True)
        return indexed

    def scatter_plot(self, data, x, y):
        # Create a scatter plot
        try:
            fig = px.scatter(
                data,
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

    def box_plot(self, data, x, y):
        # Create a box plot
        try:
            fig = px.box(
                data,
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
            return self.to_html(fig, f"box_plot_{x}_{y}.html")
        except ValueError as e:
            print(f"Error: {e}")

    def box_plot_per_postalcode(self, data, x, y):
        # Create a box plot
        try:
            for Municipality in data["Municipality"].unique():
                if data[data["Municipality"] == Municipality].shape[0] >= 10:
                    postrange = data[data["Municipality"] == Municipality][
                        "Postal Code"
                    ].unique()
                    fig = px.box(
                        data[data["Municipality"] == Municipality],
                        x=x,
                        y=y,
                        color="Type",
                        color_discrete_map={
                            "HOUSE": "red",
                            "APARTMENT": "blue",
                            "COMMERCIAL": "green",
                            "OFFICE": "purple",
                        },
                        title=f"Price vs Area in {Municipality} ({postrange.min()} - {postrange.max()})",
                        labels={
                            "Price": "Price (€)",
                            "Habitable Surface": "Area (m²)",
                        },
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
                    self.to_html(fig, f"box_plot_{x}_{y}_{Municipality}.html")
        except ValueError as e:
            print(f"Error: {e}")

    def to_html(self, fig, path):
        # Save the plot as an HTML file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        newpath = os.path.join(current_dir, "..", "data", "cleaned", path)
        fig.write_html(newpath)

    def to_html(self, fig, path):
        # Save the plot as an HTML file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        newpath = os.path.join(current_dir, "..", "data", "cleaned", path)
        fig.write_html(newpath)
