from src.clean import Clean


def main():
    # Create an instance of the Cleaned class
    clean = Clean()
    # Load the data
    clean.append_data(clean.load_data("rawdata.csv"))
    dataframe = clean.load_appended_data("appended_data.csv")
    clean.box_plot_per_postalcode(dataframe, "Type", "Price")


if __name__ == "__main__":
    main()
