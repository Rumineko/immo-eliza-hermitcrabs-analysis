import numpy as np
import pandas as pd
import plotly.express as px
import os
from pandas import DataFrame


def load_data(path: str) -> DataFrame:
    # Import Data and Convert it into a DataFrame
    current_dir = os.path.dirname(os.path.abspath(__file__))
    newpath = os.path.join(current_dir, "data", "raw", path)
    df = pd.read_csv(newpath)
    df.drop_duplicates(subset="ID", inplace=True)
    df.set_index("ID", drop=True, inplace=True)
    return df


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


def append_data(df: DataFrame) -> DataFrame:
    # Append new data to the existing data
    current_dir = os.path.dirname(os.path.abspath(__file__))
    postals = pd.read_csv(os.path.join(current_dir, "src", "zipcodes.csv"))
    for postalcode in df["Postal Code"]:
        municipality = postals[postals["Postcode"] == postalcode]["Hoofdgemeente"]
        province = postals[postals["Postcode"] == postalcode]["Provincie"]
        if not municipality.empty:
            df.loc[df["Postal Code"] == postalcode, "Municipality"] = (
                municipality.values[0]
            )
        if not province.empty:
            df.loc[df["Postal Code"] == postalcode, "Province"] = province.values[0]
    return df


def convert_non_numeric_to_numeric(df: DataFrame) -> DataFrame:
    """
    receives a dataframe and converts non-numeric columns to numeric
    """
    building_state = {
        'TO_RESTORE': 0,
        'TO_RENOVATE': 1,
        'TO_BE_DONE_UP': 2,
        'GOOD': 3,
        'JUST_RENOVATED': 4,
        'AS_NEW': 5
    }
    df['State of Building'] = df['State of Building'].apply(lambda x: building_state.get(x, np.NAN))

    energy_ratings = {
        "G": 8,
        "F": 7,
        "E": 6,
        "D": 5,
        "C": 4,
        "B": 3,
        "A": 2,
        "A+": 1,
        "A++": 0
    }
    df['EPC'] = df['EPC'].apply(lambda x: energy_ratings.get(x, np.NAN))

    kitchen_types = {
        "NOT_INSTALLED": 0,
        "USA_UNINSTALLED": 0,
        "SEMI_EQUIPPED": 1,
        "USA_SEMI_EQUIPPED": 1,
        "INSTALLED": 2,
        "USA_INSTALLED": 2,
        "HYPER_EQUIPPED": 3,
        "USA_HYPER_EQUIPPED": 3,
    }
    df['Kitchen Type'] = df['Kitchen Type'].apply(lambda x: kitchen_types.get(x, np.NAN))


    boolean = {
        False: 0,
        True: 1
    }

    df['Kitchen'] = df['Kitchen'].apply(lambda x: boolean.get(x, np.NAN))
    df['Furnished'] = df['Furnished'].apply(lambda x: boolean.get(x, np.NAN))
    df['Openfire'] = df['Openfire'].apply(lambda x: boolean.get(x, np.NAN))
    df['Terrace'] = df['Terrace'].apply(lambda x: boolean.get(x, np.NAN))
    df['Garden Exists'] = df['Garden Exists'].apply(lambda x: boolean.get(x, np.NAN))
    df['Swimming Pool'] = df['Swimming Pool'].apply(lambda x: boolean.get(x, np.NAN))
    return df


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
    converted_data = convert_non_numeric_to_numeric(appended_data)
    # output to file
    converted_data.to_csv("appended_data.csv")


if __name__ == "__main__":
    main()
