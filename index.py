import traceback
from http.client import ImproperConnectionState

import dash
import dash_design_kit as ddk
import plotly.express as px
from dash import Input, Output, State, dash_table, dcc, html

import pages
import utils
from app import app, snap

server = app.server
celery_instance = snap.celery_instance


def snapshot_modal_content():
    return html.Div(
        id="snapshot-modal-content",
        style={
            "width": "30%",
        },
        children=[
            html.P("Enter name"),
            dcc.Input(
                id="modal-username",
                placeholder="Enter name",
            ),
            html.Div(style={"height": "30px"}),
            html.P("Select a background"),
            dcc.Dropdown(
                id="modal-background",
                options=[{"label": k, "value": k} for k in utils.data_utils.get_geoheatmap_options().keys()][1:],
                value="Knowledge",
            ),
            html.Div(style={"height": "30px"}),
            html.P("Select a country"),
            dcc.Dropdown(
                id="modal-country",
                options=[{"label": k, "value": k} for k in utils.data_utils.get_raw_data().iloc[:, 3:43].columns.values.tolist()],
                value="Algeria",
            ),
            html.Div(style={"height": "30px"}),
            html.P("Include data table?"),
            dcc.RadioItems(
                id="modal-table",
                options=[
                    {"label": "Yes", "value": 1},
                    {"label": "No", "value": 0},
                ],
                value=0,
                labelStyle={"display": "inline-block"},
            ),
            html.Div(style={"height": "30px"}),
            html.Button("Submit", id="take-snapshot"),
        ],
    )


app.layout = ddk.App(
    children=[
        ddk.Header(
            [
                dcc.Link(
                    href=app.get_relative_path("/"),
                    children=ddk.Logo(

                        src=app.get_asset_url(
                            "logo.png"
                        )
                    ),
                ),
                ddk.Title("Food World Cup"),
                ddk.Menu(
                    [
                        dcc.Link(
                            href=app.get_relative_path("/"), children="Home"
                        ),
                        dcc.Link(
                            href=app.get_relative_path("/Data"),
                            children="Data",
                        ),
                        dcc.Link(
                            href=app.get_relative_path("/snapshot"),
                            children="Snapshot",
                        ),
                        dcc.Link(
                            href=app.get_relative_path("/archive"),
                            children="Archive",
                        ),
                        # The button to control the snapshot
                        ddk.Modal(
                            id="snapshot-btn-modal",
                            children=[
                                html.Button(
                                    "Take Snapshot",
                                    id="take-snapshot-button",
                                    n_clicks=0,
                                ),
                            ],
                            target_id="snapshot-modal-content",
                            hide_target=True,
                        ),
                    ],
                ),
            ]
        ),
        snapshot_modal_content(),
        dcc.Location(id="url"),
        html.Div(id="content"),
    ],
    show_editor=True,
)


@app.callback(
    Output("content", "children"),
    Output("take-snapshot-button", "style"),
    Input("url", "pathname"),
)
def display_content(pathname):
    page_name = app.strip_relative_path(pathname)

    # Style parameter to disable the snapshot button depending on the page being viewed
    hidden = {"width": 0, "visibility": "hidden"}

    if not page_name:  # None or ''
        return pages.home.layout(), None
    elif page_name == "snapshot":
        return pages.snapshot.layout(), None
    elif page_name == "Data":
        return pages.Data.layout(), None
    # Redirects the the archive and logic to direct to the selected snapshot
    elif page_name == "archive":
        return pages.archive.layout(), hidden
    elif page_name.startswith("snapshot-"):
        snapshot_id = page_name
        snapshot_content = snap.snapshot_get(snapshot_id)
        return snapshot_content, hidden
    else:
        return "404", hidden


# Callback fired when "Take Snapshot" button is clicked
@app.callback(
    Output("url", "pathname"),
    Input("take-snapshot", "n_clicks"),
    State("modal-background", "value"),
    State("modal-country", "value"),
    State("modal-username", "value"),
    State("modal-table", "value"),
    prevent_initial_call=True,
)
def save_snapshot(n_clicks, background, country, username, table):
    try:
        # Submit task to save snapshot data and generate PDF in background
        title = "Overview Data for {} Background and {} Country".format(background.title(), country.title())
        # Default username
        if not username:
            username = "DosaMeister"

        # Generate the snapshot
        snapshot_id = snap.snapshot_save_async(
            save_snapshot_in_background, title, background, country, username, table
        )

        # Save metadata to display for use in the table
        snap.meta_update(snapshot_id, {"report-creator": username})
        snap.meta_update(snapshot_id, {"report-title": title})
        return app.get_relative_path("/archive")

    except Exception as e:
        traceback.print_exc()
        return dash.no_update


# Celery worker function to generate the snapshot
@snap.celery_instance.task
@snap.snapshot_async_wrapper(save_pdf=True)
def save_snapshot_in_background(title, background, country, username, table):
    # This function is called in a separate task queue managed by celery
    # This function's parameters (temperature, pressure, humidity) are
    # provided by the callback above with `snap.snapshot_save_async`

    # Whatever is returned by this function will be saved to the database
    # with the `snapshot_id`. It needs to be JSON-serializable

    # In this case, we're just returning a pandas dataframe
    # This dataframe is loaded by `snapshot.layout` and transformed
    # into a set of `ddk.Report` & `ddk.Page` components.
    # This allows you to change your `ddk.Report` & `ddk.Page` reports
    # for older datasets.

    # You could also return a `ddk.Report` etc here if you want previously
    # saved reports to not change when you deploy new changes to your
    # `ddk.Report` layout code

    return pages.snapshot.layout(
        title=title,
        client=username,
        background=background,
        country=country,
        include_table=table,
    )


if __name__ == "__main__":
    app.run_server(debug=False)
