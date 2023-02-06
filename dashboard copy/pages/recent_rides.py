from typing import NoReturn
import pandas as pd
import plotly.express as px
import psycopg2
import psycopg2.extras
import os
from dotenv import load_dotenv
import datetime
import dash
from dash import Dash, dcc, html, Output, Input, callback
from . import recent_rides_utils

dash.register_page(__name__, path='/')

TODAY = datetime.datetime.now()
TODAY_FORMATTED = datetime.datetime(TODAY.year, TODAY.month,
                                    TODAY.day, TODAY.hour, TODAY.minute, TODAY.second)
LAST_DAY = TODAY_FORMATTED - datetime.timedelta(hours=12)


# RIDES PER GENDER
gender_rider_dist = recent_rides_utils.gender_rider_count(LAST_DAY)
# print(gender_rider_dist)
rides_per_gender_fig = recent_rides_utils.rides_per_gender_plot(
    gender_rider_dist)

# DURATION PER GENDER
gender_duration_dist = recent_rides_utils.gender_duration_count(LAST_DAY)
# print(gender_duration_dist)
duration_per_gender_fig = recent_rides_utils.duration_per_gender_plot(
    gender_duration_dist)
duration_per_gender_fig

# RIDES PER AGE BRACKET
dob_per_ride_dist = recent_rides_utils.dob_per_ride(LAST_DAY)
age_dist = recent_rides_utils.extract_ages(dob_per_ride_dist)
# print(age_dist)
age_fig = recent_rides_utils.age_plot(age_dist)

# TOTAL POWER OUTPUT
total_power = recent_rides_utils.total_power_output(LAST_DAY)

# MEAN POWER OUTPUT
mean_power = recent_rides_utils.mean_power_output(LAST_DAY)


layout = html.Div([

    # Ride details Title div
    html.Div([
        # title wrapper div
        html.Div([
            # Rides Details title
            html.H1(children='Rides Stats (12 hourly):')
        ], style={"display": "inline-block", 'width': '33%'}),

        # div for last updated text / button
        html.Div([
            html.Div([
                html.Div([
                    # Average out put aggregation text
                    html.Div(id='avg-power-output-agg-id',
                             children=[
                                html.H1(
                                    children=f"Mean Power Output: {mean_power}",
                                    style={'text-align': 'center',
                                           'font-size': '18px'})
                             ])
                ], style={"display": "inline-block", 'width': '50%'}),
                html.Div([
                    # Total power output
                    html.Div(id='total-power-output-agg-id',
                             children=[
                                html.H1(
                                    children=f"Total Power Output: {total_power}",
                                    style={'text-align': 'center',
                                           'font-size': '18px'})
                             ])
                ], style={"display": "inline-block", 'width': '50%'}),
            ]),
        ], style={"display": "inline-block", 'width': '47%'}),

        # Tabs
        html.Div([
            dcc.Tabs(id="tabs-graphs", value='tab-male',
                     children=[
                         dcc.Tab(label='Pie', value='tab-pie'),
                         dcc.Tab(label='Bar', value='tab-bar'),
                     ]
                     ),
        ], style={"display": "inline-block", 'width': '20%'}),
    ]),

    # Graphs by gender div
    html.Div([
        html.Div([
            # Number of rides per gender graph
            dcc.Graph(
                id='num-rides-graph-id',
                figure=rides_per_gender_fig),
        ], style={"display": "inline-block", 'width': '50%'}),
        html.Div([
            # Duration of rides per gender
            dcc.Graph(
                id='duration-rides-graph-id',
                figure=duration_per_gender_fig),
        ], style={"display": "inline-block", 'width': '50%'}),
    ]),

    # Age aggregation graph div
    html.Div([
        # age aggregation graph div
        dcc.Graph(
            id='age-aggregation-graph-id',
            figure=age_fig),
    ]),
], style={'padding-left': '20px', 'padding-right': '20px', 'padding-top': '20px'})
