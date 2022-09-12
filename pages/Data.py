import os
from multiprocessing import Value

import dash
import dash_design_kit as ddk
import dashboard_engine as dbe
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from dash import Input, Output, dcc, html

import utils
from app import app
from utils import chart_utils, data_utils, hist_utils

df = pd.read_csv("data/data_cleaned.csv").reset_index()
df.columns.values[1] = "Index"
df.drop("Index", inplace=True, axis=1)


def layout():

    layout = ddk.App(
        ddk.Block(
            [
                ddk.Card(
                    width=100,
                    children=[
                        ddk.DataTable(
                            data=df.to_dict("records"),
                            columns=[{"name": i, "id": i} for i in df.columns],
                            style_cell={"textAlign": "left", "padding": "5px"},
                            style_table={
                                "maxHeight": "750px",
                                "overflowY": "scroll",
                            },
                            style_header={
                                "backgroundColor": "#E8DAC5",
                                "color": "black",
                                "fontWeight": "bold",
                                # 'rgb(0,0,0)', 'rgb(117, 8, 0)', 'rgb(230,0,0)', 'rgb(255,123,0)', 'rgb(255,210,0)'
                            },
                            style_data_conditional=[
                                {
                                    "if": {"state": "selected"},
                                    "backgroundColor": "inherit !important",
                                    "border": "inherit !important",
                                },
                                {
                                    "if": {"state": "active"},
                                    "backgroundColor": "inherit !important",
                                    "border": "inherit !important",
                                },
                            ],
                            style_as_list_view=True,
                            page_size=23,
                        ),
                    ],
                ),
            ]
        )
    )
    return layout
