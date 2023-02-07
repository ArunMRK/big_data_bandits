from typing import NoReturn
import os
import datetime
import dash
from dash import Dash, dcc, html, Output, Input, callback

dash.register_page(__name__, path="/")

layout = \
    html.Div([
        # Interval timers for updating graphs
        dcc.Interval(
             id="user-interval-component",
             interval=1000,
             n_intervals=0
             ),
        dcc.Interval(
            id="riders-interval-component",
            interval=60*1000,
            n_intervals=0
        ),
        dcc.Interval(
            id="interval-component",
            interval=15*1000,
            n_intervals=0
        ),

        # Title / top div
        html.Div([
            html.Div([
                html.H2(children="Current Rider: ")
            ], style={"display": "inline-block", "width": "20%"}),
            html.Div([
                html.Div([
                    html.H2(id="name-id")
                ]),
            ], style={"display": "inline-block", "width": "30%"}),
            html.Div([
                html.Div(id="user-latest-timestamp",
                         style={"float": "right", "display": "inline-block"}),
            ], style={"display": "inline-block", "width": "50%"})
        ]),

        html.Div([
            html.Hr()
        ]),

        # User details div
        html.Div([
            html.Div([
                html.Div(
                    id="age-id", style={"text-align": "center", "font-size": "20px"}),
            ], style={"display": "inline-block", "width": "25%"}),
            html.Div([
                html.Div(id="gender-id",
                         style={"text-align": "center", "font-size": "20px"}),
            ], style={"display": "inline-block", "width": "25%"}),
            html.Div([
                html.Div(id="weight-id",
                         style={"text-align": "center", "font-size": "20px"}),
            ], style={"display": "inline-block", "width": "25%"}),
            html.Div([
                html.Div(id="height-id",
                         style={"text-align": "center", "font-size": "20px"}),
            ], style={"display": "inline-block", "width": "25%"}),
        ]),

        html.Div([
            html.Hr()
        ]),

        # User stats div
        html.Div([
            html.Div([
                html.H2("Users Stats:", style={"text-align": "top"}),
                html.Div([
                    html.Div(
                        id="duration-id", style={"text-align": "center", "font-size": "20px"}),
                ], style={"display": "inline-block", "width": "33%", "justify": "center"}),
                html.Div([
                    html.Div(
                        id="bpm-id", style={"text-align": "center", "font-weight": "bold", "font-size": "20px"}),
                ], style={"display": "inline-block", "width": "33%"}),
                html.Div([
                    html.Div(id="max-heart-rate-id",
                             style={"text-align": "center", "font-size": "20px"}),
                ], style={"display": "inline-block", "width": "33%"}),
            ], style={"display": "inline-block", "width": "50%"}),

            # Wrapper for max / current
            html.Div([
                html.Div([
                    html.Div([
                        html.Div(
                            id="rpm-id", style={"text-align": "center", "font-size": "20px"}),
                    ], style={"display": "inline-block", "width": "33%"}),
                    html.Div([
                        html.Div(
                            id="user-power-id", style={"text-align": "center", "font-size": "20px"}),
                    ], style={"display": "inline-block", "width": "33%"}),
                    html.Div([
                        html.Div(
                            id="user-resistance-id", style={"text-align": "center", "font-size": "20px"}),
                    ], style={"display": "inline-block", "width": "33%"}),
                ], style={"padding-top": "20px"}),
            ], style={"display": "inline-block", "width": "50%"}),
        ], style={"padding-top": "5px"}),

        html.Div([
            html.Hr()
        ]),

        # recent rides
        html.Div([
            html.Div([
                html.H2(children="Rides Stats (12 hourly):")
            ], style={"display": "inline-block", "width": "33%", 'padding-top': '6px'}),
            html.Div(id="latest-timestamp",
                     style={"float": "right", "display": "inline-block"}),
        ]),
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.Div(id="average-power",
                             style={"text-align": "center",
                                    "font-size": "30px", 'font-size': '22px'})
                    ], style={"display": "inline-block", "width": "50%"}),
                    html.Div([
                        html.Div(id="total-power",
                             style={"text-align": "center",
                                    "font-size": "30px", 'font-size': '22px'})
                    ], style={"display": "inline-block", "width": "50%"}),
                ], style={"padding-top": '10px'}),
            ])
        ]),

        html.Div([
            html.Div([
                html.Div(id="gender-ride",
                     style={"text-align": "center",
                            "font-size": "10px"})
            ], style={"display": "inline-block", "width": "50%"}),
            html.Div([
                html.Div(id="gender-duration",
                     style={"text-align": "center",
                            "font-size": "10px"})
            ], style={"display": "inline-block", "width": "50%"}),
        ]),

        html.Div([
            html.Div(id="age",
                     style={"text-align": "center", "font-size": "30px", "padding-left": "100px", "padding-right": "100px"})
        ]),
        dcc.Interval(
            id="interval-component",
            interval=60 * 1000,
            n_intervals=0
        )
    ], style={"padding-left": "20px", "padding-right": "20px", "padding-top": "20px"})
