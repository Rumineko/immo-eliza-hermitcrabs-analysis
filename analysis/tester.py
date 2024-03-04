import numpy as np
import pandas as pd

from src.clean import Clean


def parse_year(year):
    return pd.to_datetime(str(year), format='%Y')


immo_df = pd.read_csv('../data/cleaned/appended_data.csv')
map = {
    'TO_RESTORE': 1,
    'TO_RENOVATE': 2,
    'TO_BE_DONE_UP': 3,
    'GOOD': 4,
    'JUST_RENOVATED': 5,
    'AS_NEW': 6
}
immo_df['State of Building'] = immo_df['State of Building'].apply(lambda x: map.get(x, np.NAN))

energy_ratings = {
    "G": 0,
    "F": 1,
    "E": 2,
    "D": 3,
    "C": 4,
    "B": 5,
    "A": 6,
    "A+": 7,
    "A++": 8
}
immo_df['EPC'] = immo_df['EPC'].apply(lambda x: energy_ratings.get(x, np.NAN))
kitchen_types={
    "NOT_INSTALLED": 1,
    "USA_UNINSTALLED": 1,
    "SEMI_EQUIPPED": 2,
    "USA_SEMI_EQUIPPED": 2,
    "INSTALLED": 3,
    "USA_INSTALLED": 3,
    "HYPER_EQUIPPED": 4,
    "USA_HYPER_EQUIPPED": 4,
}
immo_df['Kitchen Type'] = immo_df['Kitchen Type'].apply(lambda x: kitchen_types.get(x, np.NAN))
# export to csv
immo_df.to_csv('../data/cleaned/data_gerrit.csv', index=False)

# prevent print of data frame trunking
pd.set_option('display.max_columns', None)
subset = immo_df.loc[:,['EPC', 'State of Building', 'Kitchen Type']]
print(subset.to_string(max_cols=None))

common_columns = ['Room Count', 'Habitable Surface', 'Build Year', "Kitchen Type", 'EPC', 'State of Building']
house_columns = ["Facades", 'Swimming Pool', 'Land Surface', ]
appartment_columns = ["Terrace Surface", "Kichen Surface"]



