import os

import dash_design_kit as ddk
import numpy as np
import pandas as pd
import plotly.express as px
from matplotlib.pyplot import figure

# Cleaned data file
data = pd.read_csv(os.path.join("data", "data_cleaned.csv"), index_col=False)
df = pd.read_csv(os.path.join("data", "data_cleaned.csv"), index_col=False)


# Function to return raw data
def get_raw_data():
    return data


# Function for the sunburst plot
def data_full():
    data_figure = data.iloc[:, [2, 3, 44, 45, 46, 47, 48]]
    data_figure = data_figure.dropna()
    # print(data_figure.to_markdown())
    return data_figure


# Function for creating a new temp table for histogram
def hist_tables(parameter):
    figure_data = data.iloc[:, 2:3]
    figure_data = figure_data.join(df[[parameter]])
    figure_data = (
        figure_data.groupby(["Knowledge", parameter])
        .size()
        .reset_index(name="Total Ratings")
    )
    column_2 = "Ratings of " + parameter
    figure_data.columns = ["Knowledge", column_2, "Total Ratings"]

    # print(figure_data.to_markdown())
    return figure_data


"""
Data table now looks like this:
|    | Knowledge    |   Ratings of Iran |   Total Ratings |
|---:|:-------------|------------------:|----------------:|
|  0 | Advanced     |                 1 |               1 |
|  1 | Advanced     |                 2 |              10 |
|  2 | Advanced     |                 3 |              30 |
|  3 | Advanced     |                 4 |              37 |
|  4 | Advanced     |                 5 |              12 |
|  5 | Expert       |                 1 |               3 |
|  6 | Expert       |                 2 |               1 |
|  7 | Expert       |                 3 |               5 |
|  8 | Expert       |                 4 |               7 |
|  9 | Expert       |                 5 |               2 |
| 10 | Intermediate |                 1 |              13 |
| 11 | Intermediate |                 2 |              30 |
| 12 | Intermediate |                 3 |              46 |
| 13 | Intermediate |                 4 |              54 |
| 14 | Intermediate |                 5 |              10 |
| 15 | Novice       |                 1 |               8 |
| 16 | Novice       |                 2 |              11 |
| 17 | Novice       |                 3 |              15 |
| 18 | Novice       |                 4 |              10 |
| 19 | Novice       |                 5 |               3 |
"""
