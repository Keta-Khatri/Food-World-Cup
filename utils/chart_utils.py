import dash_design_kit as ddk
import pandas as pd
import plotly.express as px
from matplotlib.pyplot import figure

from utils import data_utils


# Function to get the pie chart data
def generate_pie_chart(pi_background, country):
    figure_data = data_utils.get_raw_data()
    figure_data = figure_data[[pi_background, country]]
    figure_data = figure_data.groupby([pi_background])[country].mean().to_frame().reset_index()
    return figure_data

# Function to get data table for snapshots
def generate_table(df):
    df = df.head(25)
    table = ddk.DataTable(
        data=df.to_dict("records"),
        columns=[{"name": i, "id": i} for i in df.columns],
        page_action="none"
    )
    return table
