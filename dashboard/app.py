from dash import Dash, dcc, html, Output, Input
import dash
import dash_bootstrap_components as dbc
import datetime
from recent_rides_utils import *
import json
import boto3
from kafka_consumer import *
from current_ride_utils import *
from read_in_from_kafka import *
import math

app = Dash(__name__, external_stylesheets=[
           dbc.themes.ZEPHYR], use_pages=True)
app.layout = html.Div(dash.page_container)

conn = get_db_connection()

s3_client = boto3.client("s3")

def get_formatted_times() -> list[datetime.datetime, datetime.datetime]:
    TODAY = datetime.datetime.now()
    TODAY_FORMATTED = datetime.datetime(TODAY.year, TODAY.month,
                                        TODAY.day, TODAY.hour, TODAY.minute, TODAY.second)
    LAST_DAY = TODAY_FORMATTED - datetime.timedelta(hours=12)
    return [TODAY_FORMATTED, LAST_DAY]

def read_from_s3() -> dict:
    """Loads data from an S3 bucket and returns a dictionary of the users details
    """
    S3_BUCKET_NAME = "big-data-bandits"
    KEY = "current-user/user-data.json"
    s3_client = boto3.client("s3")
    response = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=KEY)
    data = response["Body"].read()
    user_details = json.loads(data)
    return user_details


@app.callback(
    [
        Output(component_id="duration-id", component_property="children"),
        Output(component_id="bpm-id", component_property="children"),
        Output(component_id="rpm-id", component_property="children"),
        Output(component_id="user-resistance-id",
               component_property="children"),
        Output(component_id="user-power-id",
               component_property="children"),
        Output(component_id="bpm-id", component_property="style")
    ],
    [Input("interval-component", "n_intervals")]
)
def run_consumer(interval: int) -> str:
    """Reads data from the Kafka stream"""
    reading = read_in_from_kafka()
    if reading:
        duration = str(reading["duration"])
        bpm = reading["current_heart_rate"]
        rpm = reading["current_rpm"]
        resistance = reading["current_resistance"]
        power = math.floor(reading["current_power"])
        max_heart_rate = read_from_s3()["max_hrt"]
        if bpm >= max_heart_rate:
            style = {"text-align": "center", "font-weight": "bold",
                     "font-size": "20px", "color": "red"}
        else:
            style = {"text-align": "center", "font-weight": "bold",
                     "font-size": "20px", "color": "green"}

    return f"{duration} seconds", f"{bpm} BPM", f"{rpm} RPM", f"{resistance} resistance", f"{power} W", style


@app.callback(
    [
        Output(component_id="name-id", component_property="children"),
        Output(component_id="age-id", component_property="children"),
        Output(component_id="gender-id", component_property="children"),
        Output(component_id="weight-id", component_property="children"),
        Output(component_id="height-id", component_property="children"),
        Output(component_id="max-heart-rate-id", component_property="children")
    ],
    [Input("user-interval-component", "n_intervals")]
)
def update_user_details(interval: int) -> tuple:
    """Reads user details from an S3 bucket and returns a string"""
    user_details = read_from_s3()

    return f"""{user_details["name"]}""", f"""{user_details["age"]} years old""", \
        f"""{(user_details["gender"]).capitalize()}""", f"""{user_details["weight"]} kg""",\
        f"""{user_details["height"]} cm""", f"""Max Threshold BPM {user_details["max_hrt"]}"""

@app.callback(
    [Output(component_id="date", component_property="children")],
    [Input("riders-interval-component", "n_intervals")]
)
def update_date(n):
    """Updates the date for the ride details title"""
    TODAY, LAST_DAY = get_formatted_times()
    return [f"{LAST_DAY} - {TODAY}"]

@app.callback(
    [Output(component_id="latest-timestamp", component_property="children")],
    [Input("riders-interval-component", "n_intervals")]
)
def update_timestamp(interval: int) -> list:
    """Updates the last updated timestamp at given intervals"""
    TODAY, LAST_DAY = get_formatted_times()

    return [html.Span(f"Last updated: {TODAY}")]


@app.callback(
    [Output(component_id="user-latest-timestamp", component_property="children")],
    [Input("interval-component", "n_intervals"), ]
)
def update_timestamp(interval: int) -> list:
    """Updates the last updated timestamp at given intervals"""
    TODAY, LAST_DAY = get_formatted_times()

    return [html.Span(f"Last updated: {TODAY}")]


@app.callback(
    [Output(component_id="total-power", component_property="children")],
    [Input("riders-interval-component", "n_intervals")]
)
def update_total_power(interval: int) -> list:
    """Updates the total power of the rides for the last 12 hours"""
    TODAY, LAST_DAY = get_formatted_times()
    cut_off = LAST_DAY
    total_power = total_power_output(cut_off)

    return [html.Span(f"Total Power Output: {total_power} W")]


@app.callback(
    [Output(component_id="average-power", component_property="children")],
    [Input("riders-interval-component", "n_intervals")]
)
def update_mean_power(interval: int) -> list:
    """Updates the mean total power output of the rides for the last 12 hours"""
    TODAY, LAST_DAY = get_formatted_times()
    mean_power = mean_power_output(LAST_DAY)

    return [html.Span(f"Mean Total Power Output: {mean_power} W")]


@app.callback(
    [Output(component_id="gender-ride", component_property="children")],
    [Input("riders-interval-component", "n_intervals")]
)
def update_rides_per_gender(interval: int) -> list:
    """Updates the distribution of genders per ride for the last 12 hours"""
    TODAY, LAST_DAY = get_formatted_times()
    gender_rider_dist = gender_rider_count(LAST_DAY)
    rides_per_gender_fig = rides_per_gender_plot(
        gender_rider_dist)

    return [dcc.Graph(figure=rides_per_gender_fig,  style={"text-align": "center", "font-size": "10px"})]


@app.callback(
    [Output(component_id="gender-duration", component_property="children")],
    [Input("riders-interval-component", "n_intervals")]
)
def update_duration_per_gender(interval: int) -> list:
    """Updates the total duration per gender for the last 12 hours"""
    TODAY, LAST_DAY= get_formatted_times()
    gender_duration_dist = gender_duration_count(LAST_DAY)
    duration_per_gender_fig = duration_per_gender_plot(
        gender_duration_dist)

    return [dcc.Graph(figure=duration_per_gender_fig, style={"text-align": "center", "font-size": "10px"})]


@app.callback(
    [Output(component_id="age", component_property="children")],
    [Input("riders-interval-component", "n_intervals")]
)
def update_ages(interval: int) -> list:
    """Updates the distribution of ages for the last 12 hours"""
    TODAY, LAST_DAY = get_formatted_times()
    dob_per_ride_dist = dob_per_ride(LAST_DAY)
    age_dist = extract_ages(dob_per_ride_dist)
    age_fig = age_plot(age_dist)

    return [dcc.Graph(figure=age_fig, style={"text-align": "center",
            "font-size": "10px"})]


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", debug=True, port=8080)
