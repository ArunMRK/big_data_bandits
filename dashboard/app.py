from dash import Dash, dcc, html, Output, Input
import plotly.express as px
import pandas as pd
import psycopg2
import psycopg2.extras
import os
from dotenv import load_dotenv
import dash


app = Dash(__name__)  # use_pages=True)

app.layout = \
    html.Div([
        # Interval timers for updating graphs
        dcc.Interval(
             id='user-interval-component',
             interval=60,
             n_intervals=0
             ),
        dcc.Interval(
            id='rides-interval-component',
            interval=60*15,
            n_intervals=0
        ),

        # Title / top div
        html.Div([
            # title wrapper div
            html.Div([
                html.H1(children='Current Riders Stats:')
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
                html.Div(id='name-id'),
            ], style={"display": "inline-block", 'width': '30%'}),
            html.Div([
                # age
                html.Div(id='age-id'),
            ], style={"display": "inline-block", 'width': '20%'}),
            html.Div([
                # gender
                html.Div(id='gender-id'),
            ], style={"display": "inline-block", 'width': '20%'}),
            html.Div([
                # weight
                html.Div(id='weight-id'),
            ], style={"display": "inline-block", 'width': '15%'}),
            html.Div([
                # height
                html.Div(id='height-id'),
            ], style={"display": "inline-block", 'width': '15%'}),
        ]),

        # Horizontal row
        html.Div([
            html.Hr()
        ]),

        # User stats div
        html.Div([
            # Wrapper
            html.Div([
                html.H2('Users Stats'),
                html.Div([
                    # Duration
                    html.Div(id='duration-id'),
                ], style={"display": "inline-block", 'width': '33%', 'justify': 'center'}),
                html.Div([
                    # BPM
                    html.Div(id='bpm-id'),
                ], style={"display": "inline-block", 'width': '33%'}),
                html.Div([
                    # Total Power
                    html.Div(id='user-total-power-id'),
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
                        html.Div(id='rpm-id'),
                    ], style={"display": "inline-block", 'width': '33%'}),
                    html.Div([
                        # current/max Power
                        html.Div(id='user-power-id'),
                    ], style={"display": "inline-block", 'width': '33%'}),
                    html.Div([
                        # current/max Resistance
                        html.Div(id='user-resistance-id'),
                    ], style={"display": "inline-block", 'width': '33%'}),
                ], style={'padding-top': '20px'}),
            ], style={"display": "inline-block", 'width': '50%'}),
        ], style={'padding-top': '10px'}),

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
            ], style={"display": "inline-block", 'width': '70%'}),
            # div for last updated text / button
            html.Div([
                html.Div([
                    # last updated text ('last updated 30 seconds ago..')
                ]),
                html.Div([
                    dcc.Tabs(id="tabs-graphs", value='tab-male',
                             children=[
                                 dcc.Tab(label='Pie', value='tab-pie'),
                                 dcc.Tab(label='Bar', value='tab-bar'),
                             ]
                             ),
                ]),
            ], style={"display": "inline-block", 'width': '30%'}),
        ]),

        # Aggregations summary div
        html.Div([
            html.Div([
                # Average out put aggregation text
                html.Div(id='avg-power-output-agg-id', style={'text-align':'center'})
            ], style={"display": "inline-block", 'width': '50%'}),
            html.Div([
                # Total power output
                html.Div(id='total-power-output-agg-id', style={'text-align':'center'})
            ], style={"display": "inline-block", 'width': '50%'}),
        ], style={'padding-top':'20px'}),

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

# update name


@app.callback(
    Output(component_id='name-id', component_property='children'),
    Input('user-interval-component', 'n_intervals'),
)
def update_name_div(n):

    name = 'Ben Douglas-Griffiths'
    return f'{name}'

# update name


@app.callback(
    Output(component_id='age-id', component_property='children'),
    Input('user-interval-component', 'n_intervals'),
)
def update_age_div(n):
    age = '24'
    return f'{age} years old'

# update gender


@app.callback(
    Output(component_id='gender-id', component_property='children'),
    Input('user-interval-component', 'n_intervals'),
)
def update_gender_div(n):
    gender = 'Male'
    return f'{gender}'

# update weight


@app.callback(
    Output(component_id='weight-id', component_property='children'),
    Input('user-interval-component', 'n_intervals'),
)
def update_weight_div(n):
    weight = '80'
    return f'{weight}KG'

# update Height


@app.callback(
    Output(component_id='height-id', component_property='children'),
    Input('user-interval-component', 'n_intervals'),
)
def update_height_div(n):
    height = '1.8'
    return f'{height}m'


# Update current users ride's statistics

# update duration
@app.callback(
    Output(component_id='duration-id', component_property='children'),
    Input('user-interval-component', 'n_intervals'),
)
def update_duration_div(n):
    duration = '240'
    return f'{duration} seconds'

# update duration
@app.callback(
    Output(component_id='bpm-id', component_property='children'),
    Input('user-interval-component', 'n_intervals'),
)
def update_bpm_div(n):
    bpm = '92'
    return f'{bpm} BPM'


# update total power
@app.callback(
    Output(component_id='user-total-power-id', component_property='children'),
    Input('user-interval-component', 'n_intervals'),
)
def update_power_div(n):
    total_power = '900'
    return f'{total_power} W'

# User stats updated by the choice of tab

# update user power
@app.callback(
    Output(component_id='user-power-id', component_property='children'),
    [Input('tabs-current-max', 'value'),
    Input('user-interval-component', 'n_intervals') ]
)
def update_bpm_div(tab, n):
    if tab == 'tab-current':
        user_power = '30'
        return f'{user_power} W'
    user_power = '50'
    return f'{user_power} W'

# update user RPM
@app.callback(
    Output(component_id='rpm-id', component_property='children'),
    [Input('tabs-current-max', 'value'),
    Input('user-interval-component', 'n_intervals')]
)
def update_rpm_div(tab, n):
    if tab == 'tab-current':
        rpm = '30'
        return f'{rpm} RPM'
    rpm = '60'
    return f'{rpm} RPM'

# update user resistance
@app.callback(
    Output(component_id='user-resistance-id', component_property='children'),
    [ Input('tabs-current-max', 'value'),
     Input('user-interval-component', 'n_intervals') ]
)
def update_rpm_div(tab, n):
    if tab == 'tab-current':
        resistance = '30'
        return f'{resistance}'
    resistance = '50'
    return f'{resistance}'
    

# Update Text for AGGREGATEs

# update user power output average
@app.callback(
    Output(component_id='avg-power-output-agg-id', component_property='children'),
    Input('rides-interval-component', 'n_intervals'),
)
def update_rpm_div(n):
    average_power_output = '30'
    return f'Average Power output: {average_power_output} W'

# total power aggregate
@app.callback(
    Output(component_id='total-power-output-agg-id', component_property='children'),
    Input('rides-interval-component', 'n_intervals')
)
def update_rpm_div(n):
    total_power_output = '200'
    return f'Total Power output: {total_power_output} W'


# Update Graphs 

# duration of rides split by gender graphs
@app.callback(
    Output(component_id='duration-rides-graph-id', component_property='figure'),
    [Input('tabs-graphs', 'value'),
    Input('rides-interval-component', 'n_intervals')]
)
def update_rpm_div(tab ,n):
    if tab == 'Pie':
        # RETURN PIE GRAPH FOR average duration split by gender
        return 
    # RETURN BAR GRAPH FOR average duration split by gender
    return

# avg number of of rides split by gender
@app.callback(
    Output(component_id='num-rides-graph-id', component_property='figure'),
    [Input('tabs-graphs', 'value'),
    Input('rides-interval-component', 'n_intervals')]
)
def update_rpm_div(tab ,n):
    if tab == 'Pie':
        # RETURN PIE GRAPH FOR number of rides split by gender
        return 
    # RETURN BAR GRAPH FOR average number of rides split by gender
    return

# avg number of of rides split by gender
@app.callback(
    Output(component_id='age-aggregation-graph-id', component_property='figure'),
    Input('rides-interval-component', 'n_intervals')
)
def update_rpm_div(n):
    # GRAPH FOR AGE DISTRIBUTION OF RIDES
    return



"""Putting this here for now, to test locally"""
if __name__ == "__main__":
    app.run_server(host="0.0.0.0", debug=True, port=8080)

  # html.Div(children=[
    #     html.H1('DELOTON'),
    #     html.Div(
    #         [
    #             html.Div(
    #                 dcc.Link(
    #                     f"{page['name']} - {page['path']}", href=page["relative_path"]
    #                 )
    #             )
    #             for page in dash.page_registry.values()
    #         ]
    #     ),
    #     dash.page_container
    # ])
