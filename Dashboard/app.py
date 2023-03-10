import dash
import dash_bootstrap_components as dbc
import datetime
import json
import math
import os
import uuid
from kafka_consumer import *
from current_ride_utils import *
from read_in_from_kafka import *
from confluent_kafka import Consumer
from recent_rides_utils import *
from dash import Dash, dcc, html, Output, Input
from dotenv import load_dotenv


load_dotenv(override=True, verbose=True)

def kafka_consumer() -> Consumer:
    """Makes a connection to a Kafka consumer"""
    c = Consumer({
        "bootstrap.servers": os.getenv("BOOTSTRAP_SERVERS"),
        "group.id": f"deloton_stream" + str(uuid.uuid1()),
        "security.protocol": "SASL_SSL",
        "sasl.mechanisms": "PLAIN",
        "sasl.username": os.getenv("SASL_USERNAME"),
        "sasl.password": os.getenv("SASL_PASSWORD"),
        "fetch.wait.max.ms": 6000,
        "auto.offset.reset": "latest",
        "enable.auto.commit": "false",
        "max.poll.interval.ms": "86400000",
        "topic.metadata.refresh.interval.ms": "-1",
        "client.id": "id-002-0068fsc",
    })
    c.subscribe(["deloton"])
    return c

consumer = kafka_consumer()
conn = get_db_connection()


app = Dash(__name__, external_stylesheets=[
           dbc.themes.ZEPHYR], use_pages=True)
app.layout = html.Div(dash.page_container)

conn = get_db_connection()
s3_client = boto3.client("s3")

def kafka_consumer() -> Consumer:
    """Makes a connection to a Kafka consumer"""
    c = Consumer({
        "bootstrap.servers": os.getenv("BOOTSTRAP_SERVERS"),
        "group.id": f"deloton_stream" + str(uuid.uuid1()),
        "security.protocol": "SASL_SSL",
        "sasl.mechanisms": "PLAIN",
        "sasl.username": os.getenv("SASL_USERNAME"),
        "sasl.password": os.getenv("SASL_PASSWORD"),
        "fetch.wait.max.ms": 6000,
        "auto.offset.reset": "latest",
        "enable.auto.commit": "false",
        "max.poll.interval.ms": "86400000",
        "topic.metadata.refresh.interval.ms": "-1",
        "client.id": "id-002-0068fsc",
    })
    c.subscribe(["deloton"])
    return c

consumer = kafka_consumer()


def get_formatted_times() -> datetime.datetime:
    TODAY = datetime.datetime.now()
    TODAY_FORMATTED = datetime.datetime(TODAY.year, TODAY.month,
                                        TODAY.day, TODAY.hour, TODAY.minute, TODAY.second)
    LAST_DAY = TODAY_FORMATTED - datetime.timedelta(hours=12)

    return TODAY_FORMATTED, LAST_DAY


def read_from_s3() -> dict:
    """Loads data from an S3 bucket and returns a dictionary of the users details
    """
    S3_BUCKET_NAME = "big-data-bandits"
    KEY = "current-user/user-data.json"
    response = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=KEY)
    data = response["Body"].read()
    user_details = json.loads(data)

    return user_details


@app.callback(
    [   Output(component_id="name-id", component_property="children"),
        Output(component_id="age-id", component_property="children"),
        Output(component_id="gender-id", component_property="children"),
        Output(component_id="weight-id", component_property="children"),
        Output(component_id="height-id", component_property="children"),
        Output(component_id="max-heart-rate-id", component_property="children"),
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

def run_consumer(interval: int) -> tuple:
    """Reads data from the Kafka stream"""
    reading, user_details = read_in_from_kafka(consumer)
    # dealing with bike data
    if reading:
        duration = reading["duration"]
        bpm = reading["current_heart_rate"]
        rpm = reading["current_rpm"]
        resistance = reading["current_resistance"]
        power = math.floor(reading["current_power"])
        max_heart_rate = read_from_s3()["max_hrt"]

        # update style if heart rate is too high
        if bpm >= max_heart_rate:
            style = {"text-align": "center", "font-weight": "bold",
                     "font-size": "20px", "color": "red"}
        else:
            style = {"text-align": "center", "font-weight": "bold",
                     "font-size": "20px", "color": "green"}
    # if no user found, do not update user details

    if user_details:
        return f"""{user_details["name"]}""", f"""{user_details["age"]} years old""", \
        f"""{(user_details["gender"]).capitalize()}""", f"""{user_details["weight"]} kg""",\
        f"""{user_details["height"]} cm""", f"""Max Threshold BPM {user_details["max_hrt"]}""",\
        f""""{duration} seconds""", f"""{bpm} BPM""", f"""{rpm} RPM""", f"""{resistance} resistance""",\
        f"""{power} W""", style

    return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update,\
            f"{duration} seconds", f"{bpm} BPM", f"{rpm} RPM", f"{resistance} resistance", f"{power} W", style
   

@app.callback(
    [Output(component_id="date", component_property="children")],
    [Input("riders-interval-component", "n_intervals")]
)
def update_date(interval: int) -> list:
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
    TODAY, LAST_DAY = get_formatted_times()
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
