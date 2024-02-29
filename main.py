from src.clean import Clean


def main():
    # Create an instance of the Cleaned class
    clean = Clean()
    # Load the data
    dataframe = clean.load_data("rawdata.csv")
    clean.scatter_plot(dataframe, "Price", "Habitable Surface")


if __name__ == "__main__":
    main()
