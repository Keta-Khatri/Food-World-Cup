"""
A basic snapshot layout
"""

from datetime import datetime

import dash_design_kit as ddk
import plotly.express as px
from dash import dcc, html

from app import app
from utils import chart_utils, data_utils, hist_utils


def footer(client):
    standard_footer = ddk.PageFooter(
        [
            html.Span(
                "Produced by {} -- Permission required for redistribution".format(
                    client
                ),
                className="note-1",
            ),
        ],
        display_page_number=True,
    )
    return standard_footer


def table_page(client, background):
    data = data_utils.get_raw_data()
    df = data.iloc[:, 3:43]
    df = df.join(data[[background]])

    page = ddk.Page(
        [ddk.SectionTitle("Table of values"), chart_utils.generate_table(df)]
    )

    return page


def section_page(title, client, bg_color="var(--accent)"):
    section = ddk.Page(
        [
            html.Div(
                title,
                style={
                    "marginTop": "2in",
                    "fontSize": "100px",
                    "fontWeight": "bold",
                    "text-align": "center",
                },
            ),
            footer(client),
        ],
        style={"backgroundColor": bg_color, "color": "#fff"},
    )

    return section


def layout(title="Food For Thought", client=None, background="Knowledge", country="Algeria", include_table=0):
    df = data_utils.get_raw_data()

    # The set of pages in the report
    children = [
        ddk.Page(
            [
                ddk.Block(
                    [
                        html.Img(
                            src=app.get_asset_url(
                                "logo.png"
                            ),
                            style={
                                "height": "auto",
                                "width": "350px",
                                "marginTop": "2.7in",
                            },
                        ),
                        html.H2(title),
                        html.H3(
                            datetime.now().strftime("%B %d, %Y"),
                            style={"margin-top": "1em"},
                        ),
                    ],
                    style={"text-align": "center"},
                ),
            ]
        ),
        ddk.Page(
            [
                ddk.SectionTitle("Backgrounds of People Survered"),
                ddk.Row(
                    [
                        ddk.Graph(
                            figure=px.sunburst(
                                data_frame=hist_utils.data_full(),
                                path=[
                                    "Location",
                                    "Household Income",
                                    "Education",
                                    "Age",
                                ],
                                color_discrete_sequence=[
                                    "rgb(0,0,0)",
                                    "rgb(117, 8, 0)",
                                    "rgb(230,0,0)",
                                    "rgb(255,123,0)",
                                    "rgb(255,210,0)",
                                ],
                            )
                        )
                    ]
                ),
                footer(client),
            ]
        ),
        ddk.Page(
            [
                ddk.SectionTitle("Histogram and Pie Chart"),
                ddk.Row(
                    [
                        ddk.Graph(
                            figure=px.histogram(
                                data_frame=hist_utils.hist_tables(country),
                                x="Knowledge",
                                y="Total Ratings",
                                color="Ratings of "+country,
                                color_discrete_sequence=['rgb(0,0,0)', 'rgb(117, 8, 0)', 'rgb(230,0,0)', 'rgb(255,123,0)', 'rgb(255,210,0)'],
                                barmode="group",
                                category_orders=dict(
                                    Knowledge=["Novice", "Intermediate", "Advanced", "Expert"],
                                    country=["1", "2", "3", "4", "5"]
                                ),
                                title="Food Knowledge of Food Ratings of "+country
                            )
                        )
                    ]
                ),
                ddk.Row(
                    [
                        ddk.Graph(
                            figure=px.pie(
                                chart_utils.generate_pie_chart(background, country),
                                values=country, names=background, hole=0.6,
                                title="Pie Chart of Food Preference Distribution for "+background+" Background",
                                color_discrete_sequence=['rgb(0,0,0)', 'rgb(230,0,0)', 'rgb(255,123,0)', 'rgb(255,210,0)']
                            )
                        )
                    ]
                ),
                ddk.SectionTitle("Food Insights"),
                ddk.Row(
                    [
                        ddk.Card(
                            [
                                ddk.Row(
                                    [
                                        html.H2(background + " with highest average food rating: ")
                                    ]
                                ),
                                ddk.Row(
                                    [
                                        html.H3(str(chart_utils.generate_pie_chart(background, country).max()[background]))
                                    ]
                                ),
                            ]
                        ),
                        ddk.Card(
                            [
                                ddk.Row(
                                    [
                                        html.H2(background + " with lowest average food rating: ")
                                    ]
                                ),
                                ddk.Row(
                                    [
                                        html.H3(str(chart_utils.generate_pie_chart(background, country).min()[background]))      
                                    ]
                                ),
                            ]
                        )
                    ]
                )
            ]
        ),
    ]

    if include_table == 1:
        children += [section_page("Table of Data", client), table_page(client, background)]

    report = ddk.Report(display_page_numbers=True, children=children)

    return report
