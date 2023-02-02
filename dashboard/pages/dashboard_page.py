from dash import Dash, dcc, html, Output, Input, callback
import plotly.express as px
import pandas as pd
import dash

dash.register_page(__name__)
layout = \
    html.Div([

        # Title / top div
        html.Div([
            # title wrapper div
            html.Div([
            ], style={"display": "inline-block", 'width': '70%'}),
            # div for last updated text
            html.Div([
                html.Div([
                    # last updated text ('last updated 30 seconds ago..')
                ]),
                html.Div([
                    # white space (lifts above div higher)
                ]),
            ], style={"display": "inline-block", 'width': '30%'}),

        ]),

        # User details div
        html.Div([
            html.Div([
                # name
            ], style={"display": "inline-block", 'width': '30%'}),
            html.Div([
                # age
            ], style={"display": "inline-block", 'width': '20%'}),
            html.Div([
                # gender
            ], style={"display": "inline-block", 'width': '20%'}),
            html.Div([
                # weight
            ], style={"display": "inline-block", 'width': '15%'}),
            html.Div([
                # height
            ], style={"display": "inline-block", 'width': '15%'}),
        ]),

        # Horizontal row
        html.Div([
            html.Hr()
        ]),

        # User stats div
        html.Div([
            html.Div([
                # Duration
            ], style={"display": "inline-block", 'width': '33%'}),
            html.Div([
                # BPM
            ], style={"display": "inline-block", 'width': '33%'}),
            html.Div([
                # Total Power
            ], style={"display": "inline-block", 'width': '33%'}),
            html.Div([
                # Vertical row
            ], style={"display": "inline-block", 'width': '33%'}),
            html.Div([
                # current/max RPM
            ], style={"display": "inline-block", 'width': '33%'}),
            html.Div([
                # current/max Power
            ], style={"display": "inline-block", 'width': '33%'}),
            html.Div([
                # current/max Resistance
            ], style={"display": "inline-block", 'width': '33%'}),
            html.Div([
                # current/max switch
            ], style={"display": "inline-block", 'width': '33%'}),

        ]),

        # Ride details Title div
        html.Div([
            # title wrapper div
            html.Div([
                # Rides Details title
            ], style={"display": "inline-block", 'width': '70%'}),
            # div for last updated text / button
            html.Div([
                html.Div([
                    # last updated text ('last updated 30 seconds ago..')
                ]),
                html.Div([
                    # pie chart / bar chart switch
                ]),
            ], style={"display": "inline-block", 'width': '30%'}),
        ]),

        # Aggregations summary div
        html.Div([
            html.Div([
                # Average out put aggregation text
            ], style={"display": "inline-block", 'width': '50%'}),
            html.Div([
                # Total power output
            ], style={"display": "inline-block", 'width': '50%'}),
        ]),

        # Graphs by gender div
        html.Div([
            html.Div([
                # Number of rides per gender graph
                dcc.Graph(
                    id='num-rides-graph-id'),
            ], style={"display": "inline-block", 'width': '50%'}),
            html.Div([
                # Duration of rides per gender
                dcc.Graph(
                    id='duration-rides-graph-id'),
            ], style={"display": "inline-block", 'width': '50%'}),
        ]),

        # Age aggregation graph div
        html.Div([
            # age aggregation graph div
            dcc.Graph(
                id='age-aggregation-graph-id'),
        ]),

    ])


# OUTPUTS for ids:

