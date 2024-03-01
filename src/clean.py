import pandas as pd
import plotly.express as px
import os

from pandas import DataFrame


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

    def exclude_outliers(self, df: DataFrame):
        # drop the row where type is not house or appartment
        df = df[df['Type'].isin(['APARTMENT', 'HOUSE']) | df['Type'].isna()]

        # drop Kitchen Surface > 100
        df = df[(df['Kitchen Surface'] < 100) | df['Kitchen Surface'].isna()]

        # drop Build year "< 1850"
        df = df[(df['Build Year'] > 1850) | df['Build Year'].isna()]

        # facades <2 -> 2, >4 -> 4
        df['Facades'] = df['Facades'].apply(lambda x: 2 if x < 2 else x)
        df['Facades'] = df['Facades'].apply(lambda x: 4 if x > 4 else x)

        # drop Bathroom Count > 4
        df = df[(df['Bathroom Count'] < 4) | df['Bathroom Count'].isna()]

        # drop bedroom count > 5
        df = df[(df['Bedroom Count'] < 5) | df['Bedroom Count'].isna()]

        # drop colum fireplace count
        df.drop(columns=['Fireplace Count'], inplace=True)

        # drop garden surface > 5000
        df = df[(df['Garden Surface'] < 5000) | df['Garden Surface'].isna()]

        # habitable surface > 700
        df = df[(df['Habitable Surface'] < 700) | df['Habitable Surface'].isna()]

        # drop Landsurface > 3000
        df = df[(df['Land Surface'] < 3000) | df['Land Surface'].isna()]

        # drop the column parking box count
        df.drop(columns=['Parking box count'], inplace=True)

        # drop items with price > 1_000_000
        df = df[(df['Price'] < 1000000) | df['Price'].isna()]

        # drop items that have sale type LIFE_ANNUITY_SALE
        df = df[df['Sale Type'] != 'LIFE_ANNUITY_SALE']

        # drop sewer column
        df.drop(columns=['Sewer'], inplace=True)

        # only keep items that have SubType == HOUSE, VILLA, TOWN_HOUSE, BUNGALOW, or not specified
        # df = df[df['Subtype'].isin(['HOUSE', 'VILLA', 'TOWN_HOUSE', 'BUNGALOW', None, '']) | df['Subtype'].isna()]

        # only keep items that have toilets of < 6
        df = df[(df['Toilet Count'] < 6) | df['Toilet Count'].isna()]

        return df


