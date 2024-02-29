from .src.clean import Clean


def main():
    # Create an instance of the Cleaned class
    clean = Clean()
    # Load the data
    data = clean.load_data("rawdata.csv")
    clean.scatter_plot(data, "x", "y")


if __name__ == "__main__":
    main()
