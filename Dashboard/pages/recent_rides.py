from typing import NoReturn
import os
import datetime
import dash
from dash import Dash, dcc, html, Output, Input, callback
from PIL import Image

dash.register_page(__name__, path="/")

pil_image = Image.open("pages/assets/Deloton-resized.png")

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
            interval=10*60*1000,
            n_intervals=0
        ),
        dcc.Interval(
            id="interval-component",
            interval=15*1000,
            n_intervals=0
        ),

        html.Div([
            html.Img(src=pil_image, style={"height": "160%", "width": "100%"})
        ]),

        # Title / top div
        html.Div([
            # title wrapper div
            html.Div([
                html.H2(children="Current Rider: ")
            ], style={"display": "inline-block", "width": "20%"}),
            # div for last updated text
            html.Div([
                html.Div([
                    html.H2(id="name-id")
                ]),
            ], style={"display": "inline-block", "width": "30%"}),
            # time stamp
            html.Div([
                html.Div(id="user-latest-timestamp",
                         style={"float": "right", "display": "inline-block"}),
            ], style={"display": "inline-block", "width": "50%"})
        ], style={"padding-top": "30px"}),

        # Horizontal rows
        html.Div([
            html.Hr()
        ]),
        html.Div([
            html.Hr()
        ]),

        # User details div
        html.Div([
            html.Div([
                # age
                html.Div(
                    id="age-id", style={"text-align": "center", "font-size": "20px"}),
            ], style={"display": "inline-block", "width": "20%"}),
            html.Div([
                # max-hrt-rate
                html.Div(id="max-heart-rate-id",
                         style={"text-align": "center", "font-size": "20px"}),
            ], style={"display": "inline-block", "width": "20%"}),
            html.Div([
                # gender
                html.Div(id="gender-id",
                         style={"text-align": "center", "font-size": "20px"}),
            ], style={"display": "inline-block", "width": "20%"}),
            html.Div([
                # weight
                html.Div(id="weight-id",
                         style={"text-align": "center", "font-size": "20px"}),
            ], style={"display": "inline-block", "width": "20%"}),
            html.Div([
                # height
                html.Div(id="height-id",
                         style={"text-align": "center", "font-size": "20px"}),
            ], style={"display": "inline-block", "width": "20%"}),
        ]),

        # Horizontal rows
        html.Div([
            html.Hr()
        ]),
        html.Div([
            html.Hr()
        ]),

        # User stats div
        html.Div([
            # Wrapper
            html.H2("Users Stats:", style={"text-align": "top"}),
            html.Div([
                # Duration
                html.Div(
                    id="duration-id", style={"text-align": "center", "font-size": "20px"}),
            ], style={"display": "inline-block", "width": "20%", "justify": "center"}),
            html.Div([
                # BPM
                html.Div(
                    id="bpm-id", style={"text-align": "center", "font-weight": "bold", "font-size": "20px"}),
            ], style={"display": "inline-block", "width": "20%"}),


            html.Div([
                # current/max RPM
                html.Div(
                    id="rpm-id", style={"text-align": "center", "font-size": "20px"}),
            ], style={"display": "inline-block", "width": "20%"}),
            html.Div([
                # current/max Power
                html.Div(
                    id="user-power-id", style={"text-align": "center", "font-size": "20px"}),
            ], style={"display": "inline-block", "width": "20%"}),
            html.Div([
                # current/max Resistance
                html.Div(
                    id="user-resistance-id", style={"text-align": "center", "font-size": "20px"}),
            ], style={"display": "inline-block", "width": "20%"}),

        ], style={"padding-top": "5px"}),

        # Horizontal row
        html.Div([
            html.Hr()
        ]),
        html.Div([
            html.Hr()
        ]),

        # Ride details Title div
        html.Div([
            # title wrapper div
            html.Div([
                # Rides Details title
                html.H2(children="Rides Stats:")
            ], style={"display": "inline-block", "width": "15%", 'padding-top': '6px'}),
            html.Div([
                html.H3(id='date')
            ], style={"display": "inline-block", "width": "60%", "padding-left": "140px"}),
            html.Div([
                html.Div(id="latest-timestamp", style={"float": "right"})
            ], style={"float": "right", "display": "inline-block"}),
        ]),
        # Power div
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        # Average out put aggregation text
                        html.Div(id="average-power",
                                 style={"text-align": "center",
                                        "font-size": "30px", 'font-size': '22px'})
                    ], style={"display": "inline-block", "width": "50%"}),
                    html.Div([
                        # Total power output
                        html.Div(id="total-power",
                                 style={"text-align": "center",
                                        "font-size": "30px", 'font-size': '22px'})
                    ], style={"display": "inline-block", "width": "50%"}),
                ], style={"padding-top": '25px'}),
            ])
        ]),
        # Horizontal row
        html.Div([
            html.Hr()
        ], style={"padding-left": "5%", "padding-right": "5%"}),

        # Graphs by gender div
        html.Div([
            html.Div([
                # Number of rides per gender graph
                html.Div(id="gender-ride")
            ], style={"display": "inline-block", "width": "33%"}),
            html.Div([
                # Duration of rides per gender
                html.Div(id="gender-duration")
            ], style={"display": "inline-block", "width": "33%"}),
            html.Div([
                html.Div(id="age")
            ], style={"display": "inline-block", "width": "33%"}),
        ], style={"padding-left": "2.5%", "padding-right": "2.5%"}),

        # Horizontal row
        html.Div([
            html.Hr()
        ]),
    ], style={"padding-left": "20px", "padding-right": "20px", "padding-top": "20px"})
