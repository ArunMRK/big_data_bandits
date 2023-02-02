from dash import Dash, dcc, html, Output, Input, callback
import plotly.express as px
import pandas as pd
import dash

dash.register_page(__name__)
layout = html.Div(children=[
    html.H1(children='Current ride'),
    html.Div([
        dcc.Dropdown(
            # TODO: Current ride graph selection
        ),
    ]),
    # TODO: grpahs here,
    html.H1(children='Recent rides'),
    dcc.Dropdown(
            # TODO: Recent ride graph selection
        ),
    #TODO: Recent ride graphs here

])