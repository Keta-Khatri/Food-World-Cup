from pydoc import describe

import dash_design_kit as ddk
import pandas as pd
import requests
from matplotlib.pyplot import figure

# Global access to data collected. Data can be manipulated during callbacks
# Initial load time high, but refresh time is minimized
data = pd.read_csv("data/food-world-cup-data.csv")

# Cleaning data to remove redundant rows
data.dropna(thresh=8, inplace=True)
data.columns = data.columns.str.replace("Please rate how much you like the traditional cuisine of ", "")
data.columns = data.columns.str.replace(".", "")

# Fetching the geojson
geojson_url = "https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson"
geojson = requests.get(geojson_url).json()

# Function to fetch raw data
def get_raw_data():
    return data

# Function to fetch the geojson
def get_geojson():
    return geojson

# Function to get geographical heatmap options
def get_geoheatmap_options():
    raw_data = get_raw_data()
    all_options = {
    "All": ["All"],
    "Knowledge": [x for x in raw_data["Knowledge"].dropna().unique()],
    "Interest": [x for x in raw_data["Interest"].dropna().unique()],
    "Gender": [x for x in raw_data["Gender"].dropna().unique()],
    "Age": [x for x in raw_data["Age"].dropna().unique()],
    "Household Income": [x for x in raw_data["Household Income"].dropna().unique()],
    "Education": [x for x in raw_data["Education"].dropna().unique()],
    "Location": [x for x in raw_data["Location"].dropna().unique()]
    }
    return all_options

# Function for geographical heatmap
def get_geoheatmap_data(background, further_background):

    figure_data = data.iloc[:, 3:43]

    # Case where a specific background is requested
    if (background != "All"):
        figure_data = figure_data.join(data[[background]])
        figure_data = figure_data[figure_data[background] == further_background]
        figure_data = figure_data.drop([background], axis=1)

    # Case for all backgrounds     
    figure_data = figure_data.mean(axis=0)
    figure_data = figure_data.to_frame().reset_index()
    figure_data.columns = ['Country', 'Rating']

    return figure_data

