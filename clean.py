import pandas as pd
import plotly.express as px
import os
from pandas import DataFrame


def load_data(path):
    # Import Data and Convert it into a DataFrame
    current_dir = os.path.dirname(os.path.abspath(__file__))
    newpath = os.path.join(current_dir, "data", "raw", path)
    data = pd.read_csv(newpath)
    data.drop_duplicates(subset="ID", inplace=True)
    data.set_index("ID", drop=True, inplace=True)
    return data


def fill_empty_data(data):
    # Fill empty values with a specific value
    data.loc[data["Swimming Pool"].isna(), "Swimming Pool"] = 0
    data.loc[data["Openfire"] == False, "Fireplace Count"] = 0
    data.loc[data["Openfire"] == True, "Fireplace Count"] = (
        data["Fireplace Count"].abs().fillna(1)
    )
    data.loc[data["Terrace"] == False, "Terrace Surface"] = 0
    data.loc[data["Garden Exists"] == False, "Garden Surface"] = 0
    return data


def append_data(data):
    # Append new data to the existing data
    current_dir = os.path.dirname(os.path.abspath(__file__))
    postals = pd.read_csv(os.path.join(current_dir, "src", "zipcodes.csv"))
    for postalcode in data["Postal Code"]:
        municipality = postals[postals["Postcode"] == postalcode]["Hoofdgemeente"]
        province = postals[postals["Postcode"] == postalcode]["Provincie"]
        if not municipality.empty:
            data.loc[data["Postal Code"] == postalcode, "Municipality"] = (
                municipality.values[0]
            )
        if not province.empty:
            data.loc[data["Postal Code"] == postalcode, "Province"] = province.values[0]
    return data


def load_appended_data(path):
    # Import Data and Convert it into a DataFrame
    current_dir = os.path.dirname(os.path.abspath(__file__))
    newpath = os.path.join(current_dir, "data", "cleaned", path)
    data = pd.read_csv(newpath)
    indexed = data.set_index("ID", drop=True)
    return indexed


def to_html(fig, path):
    # Save the plot as an HTML file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    newpath = os.path.join(current_dir, "data", "cleaned", path)
    fig.write_html(newpath)


def exclude_outliers(df: DataFrame):
    # drop the row where type is not house or appartment
    df = df[df["Type"].isin(["APARTMENT", "HOUSE"]) | df["Type"].isna()]

    # drop Kitchen Surface > 100
    df = df[(df["Kitchen Surface"] < 100) | df["Kitchen Surface"].isna()]

    # drop Build year "< 1850"
    df = df[(df["Build Year"] > 1850) | df["Build Year"].isna()]

    # facades <2 -> 2, >4 -> 4
    df["Facades"] = df["Facades"].apply(lambda x: 2 if x < 2 else x)
    df["Facades"] = df["Facades"].apply(lambda x: 4 if x > 4 else x)

    # drop Bathroom Count > 4
    df = df[(df["Bathroom Count"] < 4) | df["Bathroom Count"].isna()]

    # drop bedroom count > 5
    df = df[(df["Bedroom Count"] < 5) | df["Bedroom Count"].isna()]

    # drop colum fireplace count
    df.drop(columns=["Fireplace Count"], inplace=True)

    # drop garden surface > 5000
    df = df[(df["Garden Surface"] < 5000) | df["Garden Surface"].isna()]

    # habitable surface > 700
    df = df[(df["Habitable Surface"] < 700) | df["Habitable Surface"].isna()]

    # drop Landsurface > 3000
    df = df[(df["Land Surface"] < 3000) | df["Land Surface"].isna()]

    # drop the column parking box count
    df.drop(columns=["Parking box count"], inplace=True)

    # drop items with price > 1_000_000
    df = df[(df["Price"] < 1000000) | df["Price"].isna()]

    # drop items that have sale type LIFE_ANNUITY_SALE
    df = df[df["Sale Type"] != "LIFE_ANNUITY_SALE"]

    # drop sewer column
    df.drop(columns=["Sewer"], inplace=True)

    # only keep items that have SubType == HOUSE, VILLA, TOWN_HOUSE, BUNGALOW, or not specified
    # df = df[df['Subtype'].isin(['HOUSE', 'VILLA', 'TOWN_HOUSE', 'BUNGALOW', None, '']) | df['Subtype'].isna()]

    # only keep items that have toilets of < 6
    df = df[(df["Toilet Count"] < 6) | df["Toilet Count"].isna()]

    return df


def main():
    raw_data = load_data("rawdata.csv")
    filled_data = fill_empty_data(raw_data)
    appended_data = append_data(filled_data)


if __name__ == "__main__":
    main()
