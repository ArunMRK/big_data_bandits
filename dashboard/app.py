from dash import Dash, dcc, html, Output, Input
import plotly.express as px
import pandas as pd
import psycopg2
import psycopg2.extras
import os
from dotenv import load_dotenv
import dash
import dash_bootstrap_components as dbc
from utils import *
from kafka_consumer import *

current_ride_data = {
                    "datetime":None, "duration": None, "current_resistance": 0,
                    "current_heart_rate": 0, "current_rpm": 0, "current_power": 0,
                    "max_resistance": 0,"max_rpm": 0, "max_power": 0,
                    "total_power": 0
                }

user_details = None

app = Dash(__name__, external_stylesheets=[
           dbc.themes.COSMO])  # use_pages=True)

app.layout = \
    html.Div([
        # Interval timers for updating graphs
        dcc.Interval(
             id='user-interval-component',
             interval=60*1000,
             n_intervals=0
             ),
        dcc.Interval(
            id='rides-interval-component',
            interval=60*15*1000,
            n_intervals=0
        ),

        # Title / top div
        html.Div([
            # title wrapper div
            html.Div([
                html.H2(children='Current Rider: ')
            ], style={"display": "inline-block", 'width': '20%'}),
            # div for last updated text
            html.Div([
                html.Div([
                    # last updated text ('last updated 30 seconds ago..')
                    html.H1(id='name-id')
                ]),
                # html.Div([
                #     # white space (lifts above div higher)
                # ]),
            ], style={"display": "inline-block", 'width': '70%'}),
        ]),
        html.Div([
            html.Hr()
        ]),

        # User details div
        html.Div([
            html.Div([
                # age
                html.Div(
                    id='age-id', style={'text-align': 'center', 'font-size': '20px'}),
            ], style={"display": "inline-block", 'width': '25%'}),
            html.Div([
                # gender
                html.Div(id='gender-id',
                         style={'text-align': 'center', 'font-size': '20px'}),
            ], style={"display": "inline-block", 'width': '25%'}),
            html.Div([
                # weight
                html.Div(id='weight-id',
                         style={'text-align': 'center', 'font-size': '20px'}),
            ], style={"display": "inline-block", 'width': '25%'}),
            html.Div([
                # height
                html.Div(id='height-id',
                         style={'text-align': 'center', 'font-size': '20px'}),
            ], style={"display": "inline-block", 'width': '25%'}),
        ]),

        # Horizontal row
        html.Div([
            html.Hr()
        ]),

        # User stats div
        html.Div([
            # Wrapper
            html.Div([
                html.H2('Users Stats:', style={'text-align': 'top'}),
                html.Div([
                    # Duration
                    html.Div(
                        id='duration-id', style={'text-align': 'center', 'font-size': '20px'}),
                ], style={"display": "inline-block", 'width': '33%', 'justify': 'center'}),
                html.Div([
                    # BPM
                    html.Div(
                        id='bpm-id', style={'text-align': 'center', 'font-weight': 'bold', 'font-size': '20px'}),
                ], style={"display": "inline-block", 'width': '33%'}),
                html.Div([
                    # Total Power
                    html.Div(id='user-total-power-id',
                             style={'text-align': 'center', 'font-size': '20px'}),
                ], style={"display": "inline-block", 'width': '33%'}),
            ], style={"display": "inline-block", 'width': '50%'}),

            # Wrapper for max / current
            html.Div([

                dcc.Tabs(id="tabs-current-max", value='tab-current',
                         children=[
                             dcc.Tab(label='Current', value='tab-current'),
                             dcc.Tab(label='Max', value='tab-max'),
                         ]
                         ),
                html.Div([
                    html.Div([
                        # current/max RPM
                        html.Div(
                            id='rpm-id', style={'text-align': 'center', 'font-size': '20px'}),
                    ], style={"display": "inline-block", 'width': '33%'}),
                    html.Div([
                        # current/max Power
                        html.Div(
                            id='user-power-id', style={'text-align': 'center', 'font-size': '20px'}),
                    ], style={"display": "inline-block", 'width': '33%'}),
                    html.Div([
                        # current/max Resistance
                        html.Div(
                            id='user-resistance-id', style={'text-align': 'center', 'font-size': '20px'}),
                    ], style={"display": "inline-block", 'width': '33%'}),
                ], style={'padding-top': '20px'}),
            ], style={"display": "inline-block", 'width': '50%'}),
        ], style={'padding-top': '5px'}),

        # Horizontal row
        html.Div([
            html.Hr()
        ]),

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
                                 style={'text-align': 'center', 'font-size': '18px'})
                    ], style={"display": "inline-block", 'width': '50%'}),
                    html.Div([
                        # Total power output
                        html.Div(id='total-power-output-agg-id',
                                 style={'text-align': 'center', 'font-size': '18px'})
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
    ], style={'padding-left': '20px', 'padding-right': '20px', 'padding-top': '20px'})

# update name
@app.callback(
    Output(component_id='name-id', component_property='children'),
    Input('user-interval-component', 'n_intervals'),
)
def update_name_div(n):
    # TODO: link the name to the actual current data
    first = user_details['first']
    second = user_details['second']
    return f'{first} {second}'

# update age
@app.callback(
    Output(component_id='age-id', component_property='children'),
    Input('user-interval-component', 'n_intervals'),
)
def update_age_div(n):
     # TODO: link the age to the actual current data
    age = user_age
    return f'{age} years old'

# update gender
@app.callback(
    Output(component_id='gender-id', component_property='children'),
    Input('user-interval-component', 'n_intervals'),
)
def update_gender_div(n):
     # TODO: link the gender to the actual current data
    gender = user_details['gender']
    return f'{gender}'

# update weight
@app.callback(
    Output(component_id='weight-id', component_property='children'),
    Input('user-interval-component', 'n_intervals'),
)
def update_weight_div(n):
     # TODO: link the weight to the actual current data
    weight = user_details['weight']
    return f'{weight}KG'

# update Height
@app.callback(
    Output(component_id='height-id', component_property='children'),
    Input('user-interval-component', 'n_intervals'),
)
def update_height_div(n):
     # TODO: link the height to the actual current data
    height = user_details['height']
    return f'{height}m'


# Update current users ride's statistics

# update duration
@app.callback(
    Output(component_id='duration-id', component_property='children'),
    Input('user-interval-component', 'n_intervals'),
)
def update_duration_div(n):
     # TODO: link the duration to the actual current data
    duration = current_ride_data['duration']
    return f'{duration} seconds'

# update duration
@app.callback(
    Output(component_id='bpm-id', component_property='children'),
    Input('user-interval-component', 'n_intervals'),
)
def update_bpm_div(n):
     # TODO: link the bpm to the actual current data
    bpm = current_ride_data['current_heart_rate']
    return f'{bpm} BPM'

@app.callback(
    Output(component_id='bpm-id', component_property='style'),
    Input('user-interval-component', 'n_intervals'),
)
def update_bpm_div_color(n):
    #  TODO: CODE FOR checking heart range in healthy range
    if heart_rate >= heart_rate_abnormal:
        return {'text-align': 'center', 'font-weight': 'bold', 'font-size': '20px', 'color':'red'}
    return {'text-align': 'center', 'font-weight': 'bold', 'font-size': '20px', 'color':'green'}


# update total power
@app.callback(
    Output(component_id='user-total-power-id', component_property='children'),
    Input('user-interval-component', 'n_intervals'),
)
def update_power_div(n):
     # TODO: link the total_power to the actual current data
    total_power = current_ride_data['total_power']
    return f'{total_power} W'


# User stats updated by the choice of tab

# update user power
@app.callback(
    Output(component_id='user-power-id', component_property='children'),
    [Input('tabs-current-max', 'value'),
     Input('user-interval-component', 'n_intervals')]
)
def update_bpm_div(tab, n):
    # TODO: link the max_power / current_power to the data from actual current user
    if tab == 'tab-current':
        user_power = current_ride_data['current_power']
        return f'{user_power} W'
    user_power = current_ride_data['max_power']
    return f'{user_power} W'

# update user RPM
@app.callback(
    Output(component_id='rpm-id', component_property='children'),
    [Input('tabs-current-max', 'value'),
     Input('user-interval-component', 'n_intervals')]
)
def update_rpm_div(tab, n):
    # TODO: link the max_rpm / current_rpm to the data from actual current user
    if tab == 'tab-current':
        rpm = current_ride_data['current_rpm']
        return f'{rpm} RPM'
    rpm = current_ride_data['max_rpm']
    return f'{rpm} RPM'

# update user resistance
@app.callback(
    Output(component_id='user-resistance-id', component_property='children'),
    [Input('tabs-current-max', 'value'),
     Input('user-interval-component', 'n_intervals')]
)
def update_rpm_div(tab, n):
    # TODO: link the max_resistance / current_resistance to the data from actual current user
    if tab == 'tab-current':
        resistance = current_ride_data['current_resistance']
        return f'{resistance}'
    resistance = current_ride_data['max_resistance']
    return f'{resistance}'


# Update Text for AGGREGATEs

# update user power output average
@app.callback(
    Output(component_id='avg-power-output-agg-id',
           component_property='children'),
    Input('rides-interval-component', 'n_intervals'),
)
def update_avg_power_output_div(n):
    # TODO: link the average power output to the data from DATA WAREHOUSE
    average_power_output = '30'
    return f'Average Power output: {average_power_output} W'

# total power aggregate
@app.callback(
    Output(component_id='total-power-output-agg-id',
           component_property='children'),
    Input('rides-interval-component', 'n_intervals')
)
def update_rpm_div(n):
    # TODO: link the total power out putto the data from DATA WAREHOUSE
    total_power_output = '200'
    return f'Total Power output: {total_power_output} W'


# Update Graphs

# duration of rides split by gender graphs
@app.callback(
    Output(component_id='duration-rides-graph-id',
           component_property='figure'),
    [Input('tabs-graphs', 'value'),
     Input('rides-interval-component', 'n_intervals')]
)
def update_rpm_div(tab, n):
    if tab == 'Pie':
        # TODO: RETURN PIE GRAPH FOR average duration split by gender
        return
    # TODO: RETURN BAR GRAPH FOR average duration split by gender
    return

# avg number of of rides split by gender
@app.callback(
    Output(component_id='num-rides-graph-id', component_property='figure'),
    [Input('tabs-graphs', 'value'),
     Input('rides-interval-component', 'n_intervals')]
)
def update_rpm_div(tab, n):
    if tab == 'Pie':
        # TODO: RETURN PIE GRAPH FOR number of rides split by gender
        return
    # TODO: RETURN BAR GRAPH FOR average number of rides split by gender
    return

# avg number of of rides split by gender
@app.callback(
    Output(component_id='age-aggregation-graph-id',
           component_property='figure'),
    Input('rides-interval-component', 'n_intervals')
)
def update_rpm_div(n):
    # TODO: GRAPH FOR AGE DISTRIBUTION OF RIDES
    return


"""Putting this here for now, to test locally"""
if __name__ == "__main__":

    print('Beginning Kafka script')

    found_user = False
    ride_exists = False
    user_id = None
    heart_rate_abnormal=False
    heart_rate_counter = 0
    max_user_heart_rate = 0
    c = kafka_consumer()
    while True:
        message = get_kafka_message(c)
        if message:
            print(message)
            if "Getting user" in message:
                ''' Resetting variables for new user'''
                found_user = False
                ride_exists = False
                current_ride_data = {
                    "datetime": None, "duration": None, "current_resistance": 0,
                    "current_heart_rate": 0, "current_rpm": 0, "current_power": 0,
                    "max_resistance": 0,"max_rpm": 0, "max_power": 0,
                    "total_power": 0
                }
                heart_rate_abnormal=False
                max_user_heart_rate = 0

            elif 'user_id' in message:
                '''New user found'''
                found_user = True
                ride_exists = True
                user_details = extract_user_details(message)
                user_id = int(user_details["user_id"])
                user_age = age_from_dob(user_details["dob_date"])
                max_heart_rate = get_max_heart_rate(user_age)

            elif found_user and ("Ride - duration" in message):
                ''' get first part of data if user exists'''
                ride_duration_resistance = extract_ride_duration_resistance_data(
                    message)

                current_ride_data["duration"] = float(ride_duration_resistance["duration"])
                current_ride_data["current_resistance"] = int(ride_duration_resistance["resistance"])
                current_ride_data["datetime"]= ride_duration_resistance["date_time"]

                if current_ride_data["max_resistance"] < int(ride_duration_resistance["resistance"]):
                    current_ride_data["max_resistance"] = int(ride_duration_resistance["resistance"])
                


          
            elif found_user and ("Telemetry - hrt" in message):
                '''  get second part of data if user exists'''
                ride_hrt_rpm_power = extract_ride_hrt_rpm_power(message)
                heart_rate = int(ride_hrt_rpm_power["heart_rate"])

                if (heart_rate > max_heart_rate):
                    '''Trigger that checks the heart rate'''
                    heart_rate_abnormal=True


                current_ride_data["current_heart_rate"] = heart_rate
                current_ride_data["current_rpm"] = int(ride_hrt_rpm_power["rpm"])
                current_ride_data["current_power"] = float(ride_hrt_rpm_power["power"])
                current_ride_data["total_power"] += float(ride_hrt_rpm_power["power"])

                if current_ride_data["max_rpm"] < int(ride_duration_resistance["rpm"]):
                    current_ride_data["max_rpm"] = int(ride_duration_resistance["rpm"])
                if current_ride_data["max_power"] < int(ride_duration_resistance["power"]):
                    current_ride_data["max_power"] = int(ride_duration_resistance["power"])
                    
        app.run_server(host="0.0.0.0", debug=True, port=8080)