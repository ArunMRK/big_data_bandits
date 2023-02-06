from dash import Dash, dcc, html, Output, Input
import dash
import dash_bootstrap_components as dbc
import datetime
from recent_rides_utils import *

app = Dash(__name__, external_stylesheets=[
           dbc.themes.COSMO], use_pages=True)

app.layout = html.Div(dash.page_container)

conn = get_db_connection()

TODAY = datetime.datetime.now()
TODAY_FORMATTED = datetime.datetime(TODAY.year, TODAY.month,
                                    TODAY.day, TODAY.hour, TODAY.minute, TODAY.second)
LAST_DAY = TODAY_FORMATTED - datetime.timedelta(hours=12)


@app.callback(
    [Output(component_id="latest-timestamp", component_property="children")],
    [Input("interval-component", "n_intervals")]
)
def update_timestamp(interval) -> list:
    """Updates the last updated timestamp at given intervals"""
    TODAY = datetime.datetime.now()
    TODAY_FORMATTED = datetime.datetime(TODAY.year, TODAY.month,
                                        TODAY.day, TODAY.hour, TODAY.minute, TODAY.second)
    LAST_DAY = TODAY_FORMATTED - datetime.timedelta(hours=12)
    return [html.Span(f"Last updated: {TODAY_FORMATTED}")]


@app.callback(
    [Output(component_id="total-power", component_property="children")],
    [Input("interval-component", "n_intervals")]
)
def update_total_power(interval) -> list:
    """Updates the total power of the rides for the last 12 hours"""
    TODAY = datetime.datetime.now()
    TODAY_FORMATTED = datetime.datetime(TODAY.year, TODAY.month,
                                        TODAY.day, TODAY.hour, TODAY.minute, TODAY.second)
    LAST_DAY = TODAY_FORMATTED - datetime.timedelta(hours=12)

    cut_off = LAST_DAY
    total_power = total_power_output(cut_off)

    return [html.Span(f"Total Power Output: {total_power}")]


@app.callback(
    [Output(component_id="average-power", component_property="children")],
    [Input("interval-component", "n_intervals")]
)
def update_mean_power(interval) -> list:
    """Updates the mean total power output of the rides for the last 12 hours"""
    TODAY = datetime.datetime.now()
    TODAY_FORMATTED = datetime.datetime(TODAY.year, TODAY.month,
                                        TODAY.day, TODAY.hour, TODAY.minute, TODAY.second)
    LAST_DAY = TODAY_FORMATTED - datetime.timedelta(hours=12)
    mean_power = mean_power_output(LAST_DAY)

    return [html.Span(f"Mean Power Output: {mean_power}")]


@app.callback(
    [Output(component_id="gender-ride", component_property="children")],
    [Input("interval-component", "n_intervals")]
)
def update_rides_per_gender(interval) -> list:
    """Updates the distribution of genders per ride for the last 12 hours"""
    TODAY = datetime.datetime.now()
    TODAY_FORMATTED = datetime.datetime(TODAY.year, TODAY.month,
                                        TODAY.day, TODAY.hour, TODAY.minute, TODAY.second)
    LAST_DAY = TODAY_FORMATTED - datetime.timedelta(hours=12)
    gender_rider_dist = gender_rider_count(LAST_DAY)
    rides_per_gender_fig = rides_per_gender_plot(
        gender_rider_dist, LAST_DAY, TODAY_FORMATTED)

    return [dcc.Graph(figure=rides_per_gender_fig)]


@app.callback(
    [Output(component_id="gender-duration", component_property="children")],
    [Input("interval-component", "n_intervals")]
)
def update_duration_per_gender(interval) -> list:
    """Updates the total duration per gender for the last 12 hours"""
    TODAY = datetime.datetime.now()
    TODAY_FORMATTED = datetime.datetime(TODAY.year, TODAY.month,
                                        TODAY.day, TODAY.hour, TODAY.minute, TODAY.second)
    LAST_DAY = TODAY_FORMATTED - datetime.timedelta(hours=12)
    gender_duration_dist = gender_duration_count(LAST_DAY)
    duration_per_gender_fig = duration_per_gender_plot(
        gender_duration_dist, LAST_DAY, TODAY_FORMATTED)

    return [dcc.Graph(figure=duration_per_gender_fig)]


@app.callback(
    [Output(component_id="age", component_property="children")],
    [Input("interval-component", "n_intervals")]
)
def update_ages(interval) -> list:
    """Updates the distribution of ages for the last 12 hours"""
    TODAY = datetime.datetime.now()
    TODAY_FORMATTED = datetime.datetime(TODAY.year, TODAY.month,
                                        TODAY.day, TODAY.hour, TODAY.minute, TODAY.second)
    LAST_DAY = TODAY_FORMATTED - datetime.timedelta(hours=12)
    dob_per_ride_dist = dob_per_ride(LAST_DAY)
    age_dist = extract_ages(dob_per_ride_dist)
    age_fig = age_plot(age_dist, LAST_DAY, TODAY_FORMATTED)

    return [dcc.Graph(figure=age_fig)]


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", debug=True, port=8080)
