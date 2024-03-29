# Immo Eliza / Data Analysis

[![forthebadge made-with-python](https://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

By team **HermitCrab**

![Charlie](https://cdn.discordapp.com/attachments/1209053035783913502/1214893521212018758/Charlie_100.png?ex=66167443&is=6603ff43&hm=ffa00a8503d1d0990689c5a027e7f6eecfa360c1da4b86534789054696740159&)

[Karel](https://www.linkedin.com/in/karel-rodriguez-duran/), [Alice](https://www.linkedin.com/in/alice-edcm/), [Gerrit](https://www.linkedin.com/in/gerrit-geeraerts-143488141/), [Em](https://www.linkedin.com/in/mirunasuru/)

## 📖 Description

Clean.py is our main tool in this project, and it is responsible for multiple functions to clean and prepare data to help with data visualization:

* Imports the Raw Data from Part 1 of our Project, and appends some extra information with a few functions:
  * append_data: Adds a Municipality and Province column, by comparing the Postal Code present in each property to a list we obtained from [BPost](https://www.bpost.be/nl/postcodevalidatie-tool)'s website.
  * province_to_region: Adds a Region column, by checking previously added Province column and comparing its values.
  * price_per_sqm: Adds a Price Per Sqm column, which is calculated by dividing the price of a property by its total area (which is a sum of habitable surface, terrace surface and garden surface)
* Fills empty data values by using logical reasoning: e.g. filling empty values of Garden Surface for 0 in case Garden Exists is False.
* Converts booleans (True or False) values into numericals (1 or 0, respectively), as well as some others using other kinds of logic.

## 🛠️ Setup & Installation

- create a new virtual environment by executing this command in your terminal:
  `python3 -m venv data_analysis_env`
- activate the environment by executing this command in your terminal:
  `source data_analysis_env/bin/activate`
- install the required dependencies by executing this command in your terminal:
  `pip install -r requirements.txt`

## 👩‍💻 Usage

To run the program, clone this repo on your local machine, navigate to its directory in your terminal, make sure you have first executed your requirements.txt, then execute:

```
python3 clean.py
```

## 🗂️ File Structure

```
.
├── analysis/
│   ├── PLACEHOLDER
│   └── pygwalker.ipynb
│
├── data/
│   ├── cleaned/
│   │   └── appended_data.csv
│   └── raw/
│       └── rawdata.csv
│
├── reports/
│   └── final_presentation.pdf
│
├── src/
│   └── zipcodes.csv
│
├── .gitignore
├── clean.py
└── README.md
```

## Program Output

The end result is a lot of refined data that we utilize to study the connection between the different variables of a house/apartment and its resulting selling price. We each took our own initiative to utilize this data we refined and then studied it after discussing what kinds of graphs each of us should focus on.

## 📂 Project Background & Timeline

This data analysis project was done as part of the BeCode AI Bootcamp over the course of approximately two weeks in February-March 2024.
It is the second phase of a larger team project to build a machine learning model that predicts the price of real estate properties in Belgium.

## Thank you for Visiting our Project Page!

We are team **HermitCrab**: [Karel](https://www.linkedin.com/in/karel-rodriguez-duran/), [Alice](https://www.linkedin.com/in/alice-edcm/), [Gerrit](https://www.linkedin.com/in/gerrit-geeraerts-143488141/), [Em](https://www.linkedin.com/in/mirunasuru/)

![Charlie](https://cdn.discordapp.com/attachments/1209053035783913502/1214893521212018758/Charlie_100.png?ex=66167443&is=6603ff43&hm=ffa00a8503d1d0990689c5a027e7f6eecfa360c1da4b86534789054696740159&)
