from typing import NoReturn
import os
import datetime
import dash
from dash import Dash, dcc, html, Output, Input, callback

dash.register_page(__name__, path="/")

layout = html.Div([
    # Ride details Title div
    html.Div([
        # title wrapper div
        html.Div([
            # Rides Details title
            html.H1(children="Rides Stats (12 hourly):")
        ], style={"display": "inline-block", "width": "33%"}),
        html.Div(id="latest-timestamp",
                 style={"float": "right", "display": "inline-block"}),
    ]),
    # Power div
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    # Average out put aggregation text
                    html.Div(id="average-power",
                             style={"text-align": "center",
                                    "font-size": "30px"})
                ], style={"display": "inline-block", "width": "50%"}),
                html.Div([
                    # Total power output
                    html.Div(id="total-power",
                             style={"text-align": "center",
                                    "font-size": "30px"})
                ], style={"display": "inline-block", "width": "50%"}),
            ]),
        ])
    ]),

    # Graphs by gender div
    html.Div([
        html.Div([
            # Number of rides per gender graph
            html.Div(id="gender-ride",
                     style={"text-align": "center",
                            "font-size": "30px"})], style={"display": "inline-block", "width": "50%"}),
        html.Div([
            # Duration of rides per gender
            html.Div(id="gender-duration",
                     style={"text-align": "center",
                            "font-size": "30px"})
        ], style={"display": "inline-block", "width": "50%"}),
    ]),

    # Age aggregation graph div
    html.Div([
        # age aggregation graph div
        html.Div(id="age",
                    style={"text-align": "center", "font-size": "30px", "padding-left": "100px", "padding-right": "100px"})
    ]),
    dcc.Interval(
        id="interval-component",
        interval=60 * 1000,
        n_intervals=0
    )
], style={"padding-left": "20px", "padding-right": "20px", "padding-top": "20px"})
