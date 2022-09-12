"""
Archive table
"""
from dash import html
import dash_snapshots

from app import snap


def layout():
    return html.Div(
        [
            snap.ArchiveTable(
                columns=[
                    # Meta data options corresponds to the column displayed in archive table.
                    {
                        "id": dash_snapshots.constants.KEYS["snapshot_id"],
                        "name": "Report View",
                    },
                    {"id": dash_snapshots.constants.KEYS["pdf"], "name": "PDF",},
                    {"id": "report-title", "name": "Report Title",},
                    {"id": "report-creator", "name": "Report Creator",},
                    {
                        "id": dash_snapshots.constants.KEYS["created_time"],
                        "name": "Report Created Date",
                    },
                    {
                        "id": dash_snapshots.constants.KEYS["task_finish_time"],
                        "name": "Report Finish Date",
                    },
                ]
            )
        ]
    )
