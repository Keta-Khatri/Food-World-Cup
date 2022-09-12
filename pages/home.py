import os
from cmath import pi
from multiprocessing import Value

import dash
import dash_design_kit as ddk
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from dash import Input, Output, dcc, html

import utils
from app import app
from utils import chart_utils, data_utils, hist_utils

# HOME PAGE LAYOUT:


def layout():

    layout = html.Div(
        children=[
            dcc.Tabs(
                style={"margin": "5px", "marginBottom": "0px"},
                children=[
                    dcc.Tab(
                        label="Food Insights",
                        children=[
                            ddk.Row(
                                [
                                    ddk.Card(
                                        width=50,
                                        children=[
                                            dcc.Markdown(
                                                """
  **Information about the Data:**
> The dataset is called Food-world-cup. It shows the number what people ranked the food in different countries. 
> The knowledge column is the respondent's overall knowledge in food, the country columns are what they ranked the food in each country.

  **Ratings: **
> Here is what each rating means:
* 5 : I love this country's traditional cuisine. I think it's one of the best in the world.
* 4 : I like this country's traditional cuisine. I think it's considerably above average.
* 3 : I'm OK with this county's traditional cuisine. I think it's about average.
* 2 : I dislike this country's traditional cuisine. I think it's considerably below average.
* 1 : I hate this country's traditional cuisine. I think it's one of the worst in the world.
* N/A: I'm unfamiliar with this country's traditional cuisine.
                             """
                                            ),
                                        ],
                                    ),
                                    ddk.Card(
                                        width=50,
                                        children=[
                                            dcc.Markdown(
                                                """
**World Map plot:**
> Takes the average ratings of the countries and plots them, the darker the color, the higher the ratings.
> Uses dropdowns to show the average ratings for specific criteria

**Pie Chart:**
> Takes in a specific background category and a country to output percentages of the average ratings
> the percentages represent the preference of one category to that country's food

**Bar plot:**
> Compares the knowledge of the respondents to the rankings of the selected country. 
> If you hover on it, it shows:
* total number of knowledge specific ratings
* the rating value
* the knowledge level
                                            """
                                            ),
                                        ],
                                    ),
                                ]
                            ),
                            ddk.Row(
                                [
                                    # Geographical heatmap for average food rating for each background
                                    ddk.Card(
                                        width=50,
                                        children=[
                                            dcc.Dropdown(
                                                id="background",
                                                options=[
                                                    {"label": k, "value": k}
                                                    for k in data_utils.get_geoheatmap_options().keys()
                                                ],
                                                value="All",
                                                clearable=True,
                                                persistence=True,
                                                persistence_type="local",
                                            ),
                                            dcc.Dropdown(
                                                id="further-background",
                                                clearable=True,
                                                persistence=True,
                                                persistence_type="local",
                                            ),
                                            ddk.Graph(id="map"),
                                        ],
                                    ),
                                    # Pie chart for food preference based on background
                                    ddk.Card(
                                        width=50,
                                        children=[
                                            dcc.Dropdown(
                                                id="pi_background",
                                                options=[
                                                    {"label": k, "value": k}
                                                    for k in data_utils.get_geoheatmap_options().keys()
                                                ],
                                                value="Knowledge",
                                                clearable=True,
                                                persistence=True,
                                                persistence_type="local",
                                            ),
                                            dcc.Dropdown(
                                                id="country",
                                                options=[
                                                    {"label": k, "value": k}
                                                    for k in data_utils.get_raw_data()
                                                    .iloc[:, 3:43]
                                                    .columns.values.tolist()
                                                ],
                                                value="Algeria",
                                                clearable=True,
                                                persistence=True,
                                                persistence_type="local",
                                            ),
                                            ddk.Graph(id="piechart"),
                                        ],
                                    ),
                                ]
                            ),
                            ddk.Row(
                                [
                                    # Histogram of food knowledge by food ratings of a specific background
                                    ddk.Card(
                                        width=100,
                                        children=[
                                            dcc.Dropdown(
                                                id="column-dropdown",
                                                options=[
                                                    {"label": k, "value": k}
                                                    for k in hist_utils.get_raw_data()
                                                    .iloc[:, 4:43]
                                                    .columns.values.tolist()
                                                ],
                                                value="Algeria",
                                                persistence=True,
                                                persistence_type="local",
                                            ),
                                            ddk.Graph(id="histogram"),
                                        ],
                                    ),
                                ]
                            ),
                        ],
                    ),
                    dcc.Tab(
                        label="Surveyers' Background",
                        children=[
                            ddk.Row(
                                [
                                    ddk.Card(
                                        width=20,
                                        children=[
                                            dcc.Markdown(
                                                """
**Sunburst plot:**
> Shows the background information of the respondants.
> From inside to out, the categories are:
* Location (where the survey was taken)
* Household Income
* Education
* Age
>
> The sizes of the values are created by the number of instances in that category.
> 
                                            """
                                            )
                                        ],
                                    ),
                                    ddk.Card(
                                        width=80,
                                        children=[
                                            ddk.Graph(
                                                figure=px.sunburst(
                                                    data_frame=hist_utils.data_full(),
                                                    path=[
                                                        # "Knowledge",
                                                        "Location",
                                                        "Household Income",
                                                        "Education",
                                                        "Age",
                                                        # "Gender",
                                                        # "Interest",
                                                    ],
                                                    color_discrete_sequence=[
                                                        "rgb(0,0,0)",
                                                        "rgb(117, 8, 0)",
                                                        "rgb(230,0,0)",
                                                        "rgb(255,123,0)",
                                                        "rgb(255,210,0)",
                                                    ],
                                                ),
                                                style={
                                                    "height": 700,
                                                },
                                            )
                                        ],
                                    ),
                                ]
                            ),
                        ],
                    ),
                ],
            )
        ]
    )

    return layout


### CALLBACKS:

## Histogram of food knowledge by food ratings of a specific background

# Callback for heatmap dropdown
@app.callback(Output("histogram", "figure"), Input("column-dropdown", "value"))
def update_histogram(parameter):
    if not parameter:
        return dash.no_update
    else:
        hist_data = hist_utils.hist_tables(parameter)
        country = "Ratings of " + parameter
        title_name = "Food Knowledge by Food Ratings of " + parameter
        fig = px.histogram(
            data_frame=hist_data,
            x="Knowledge",
            y="Total Ratings",
            color=country,
            category_orders=dict(
                Knowledge=["Novice", "Intermediate", "Advanced", "Expert"],
                country=["1", "2", "3", "4", "5"],
            ),
            color_discrete_sequence=[
                "rgb(0,0,0)",
                "rgb(117, 8, 0)",
                "rgb(230,0,0)",
                "rgb(255,123,0)",
                "rgb(255,210,0)",
            ],
            barmode="group",
            title=title_name,
        )
        fig.update_yaxes(fixedrange=True, title_text="Total Ratings")

        return fig


## Geographical heatmap for average food rating for each background

# Callback for background dropdown
@app.callback(
    Output("further-background", "options"), Input("background", "value")
)
def set_further_background_options(selected_background):
    return [
        {"label": i, "value": i}
        for i in data_utils.get_geoheatmap_options()[selected_background]
    ]


# Callback for further-background dropdown
@app.callback(
    Output("further-background", "value"),
    Input("further-background", "options"),
)
def set_further_background_value(available_options):
    return available_options[0]["value"]


# Callback for generating geoheatmap
@app.callback(
    Output("map", "figure"),
    Input("background", "value"),
    Input("further-background", "value"),
)
def display_geoheatmap(background, further_background):
    # Updates geoheatmap when options are selected
    if background and further_background:
        updated_data = data_utils.get_geoheatmap_data(
            background, further_background
        )
        fig = px.choropleth_mapbox(
            updated_data,
            geojson=data_utils.get_geojson(),
            locations="Country",
            featureidkey="properties.ADMIN",
            color="Rating",
            hover_name="Country",
            title="Geographical Heatmap of Average Food Rating for "
            + background
            + " ("
            + further_background
            + ") Background(s)",
            mapbox_style="carto-positron",
            zoom=1,
            color_continuous_scale="YlOrRd",
        )
        return fig
    # Remains the same when options are unselected
    else:
        return dash.no_update


## Pie chart for food preference based on background

# Callback for pie chart based on both dropdowns
@app.callback(
    Output("piechart", "figure"),
    Input("pi_background", "value"),
    Input("country", "value"),
)
def display_piechart(pi_background, country):
    # Updates pie chart when options are selected
    if pi_background and country:
        updated_data = chart_utils.generate_pie_chart(pi_background, country)
        fig = px.pie(
            updated_data,
            values=country,
            names=pi_background,
            hole=0.6,
            title="Pie Chart of Food Preference Distribution for "
            + pi_background
            + " Background",
            color_discrete_sequence=[
                "rgb(0,0,0)",
                "rgb(230,0,0)",
                "rgb(255,123,0)",
                "rgb(255,210,0)",
            ],
        )
        return fig
    # Remains the same when options are unselected
    else:
        return dash.no_update
