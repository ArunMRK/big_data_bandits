from dotenv import load_dotenv
import os
import psycopg2.extras
import psycopg2
import plotly.express as px
import pandas as pd
import datetime
from typing import NoReturn
from dash import Dash, dcc, html, Output, Input, callback

load_dotenv(override=True, verbose=True)

# Getting Data from Aurora RDBS AWS source
RDS_DB = os.getenv("RDS_DB_NAME")
RDS_USER = os.getenv("RDS_USER")
RDS_PASSWORD = os.getenv("RDS_PASSWORD")
RDS_HOST = os.getenv("RDS_HOST")


def get_db_connection() -> psycopg2.extensions.connection:
    """ Create a connection for database postgres Aurora"""
    try:
        conn = psycopg2.connect(f"""
    dbname={RDS_DB}
    user={RDS_USER} 
    password={RDS_PASSWORD}
    host={RDS_HOST}""")
        return conn
    except:
        print("Error connecting to database.")


def query_executer(
    conn: psycopg2.extensions.connection, query: str, params: tuple = ()
) -> list:
    """An executor function for executing sql statements"""
    if conn != None:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query, params)
            conn.commit()
            try:
                returned_data = cur.fetchall()
                return returned_data
            except:
                pass
    else:
        return "No connection"


conn = get_db_connection()


def gender_rider_count(cut_off: datetime.datetime) -> pd.DataFrame:
    """Determines the unique riders and extracts all information about them into a Dataframe
    """
    sql = f"""SELECT DISTINCT user_details.gender, COUNT(*) FROM user_details 
    JOIN ride_details ON ride_details.user_id = user_details.user_id WHERE ride_details.started > '{cut_off}' GROUP BY user_details.gender;"""
    data = query_executer(conn, sql)
    colNames = data[0].keys()
    gender_rides = pd.DataFrame(
        [[row[col] for col in colNames] for row in data], columns=colNames)

    return gender_rides


def rides_per_gender_plot(data: pd.DataFrame) -> px.pie:
    """Pie plot of the gender distributions for the riders for the past 24 hours
    """
    plot_data = {"gender": list(data["gender"]), "count": list(data["count"])}

    fig = px.pie(
        plot_data, values="count", names="gender", color="gender",
        labels={
            "count": "Count",
            "gender": "Gender"
        }, title="Number of Rides per Gender"
    )
    fig.update_layout(
        font=dict(
            size=18
        ),
        title_x=0.5
    )

    return fig


def gender_duration_count(cut_off: datetime.datetime) -> pd.DataFrame:
    """Determines the unique riders and extracts all information about them into a Dataframe
    """

    sql = f"""SELECT DISTINCT user_details.gender, SUM(ride_details.duration) AS total_duration FROM user_details JOIN ride_details ON ride_details.user_id = user_details.user_id WHERE ride_details.started > '{cut_off}' GROUP BY user_details.gender;"""
    data = query_executer(conn, sql)
    colNames = data[0].keys()
    gender_duration = pd.DataFrame(
        [[row[col] for col in colNames] for row in data], columns=colNames)

    return gender_duration


def duration_per_gender_plot(data: pd.DataFrame) -> px.bar:
    """Bar plot of the gender distributions for the riders for the past 24 hours
    """
    plot_data = {"gender": list(data["gender"]),
                 "total_duration": list(data["total_duration"])}

    fig = px.bar(plot_data, x="gender", y="total_duration", color="gender",
                 labels={
                     "gender": "Gender",
                     "total_duration": "Total Duration (s)"
                 },
                 title="Total Duration per Gender"
                 )
    fig.update_layout(
        font=dict(
            size=18
        ),
        title_x=0.5
    )

    return fig


def dob_per_ride(cut_off: datetime.datetime) -> pd.DataFrame:

    sql = f"""SELECT user_details.dob_date FROM user_details JOIN ride_details ON ride_details.user_id = user_details.user_id WHERE ride_details.started > '{cut_off}';"""
    data = query_executer(conn, sql)
    colNames = data[0].keys()
    ride_dobs = pd.DataFrame(
        [[row[col] for col in colNames] for row in data], columns=colNames)

    return ride_dobs


def age_from_dob(born: datetime.date) -> int:
    """Find user's age from DOB"""
    today = datetime.date.today()

    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def age_into_brackets(age: int) -> str:
    """Puts the age into its corresponding bracket - returns the bracket"""
    if age < 18:
        return "<18"
    elif age < 25:
        return "18-24"
    elif age < 35:
        return "25-34"
    elif age < 45:
        return "35-44"
    elif age < 55:
        return "45-54"
    elif age < 65:
        return "55-64"
    else:
        return "65+"


def extract_ages(df: pd.DataFrame) -> list:
    """Extracts the ages of users from the past 24 hours and returns a list of all ages"""
    ages = df["dob_date"].apply(age_from_dob)
    # 18-24, 25-34, 35-44, 45-54, 55-64 and 65 and over
    age_brackets = {
        "<18": 0, "18-24": 0, "25-34": 0, "35-44": 0, "45-54": 0,
        "55-64": 0, "65+": 0
    }

    for age in ages:
        age_brackets[age_into_brackets(age)] += 1

    return age_brackets


def age_plot(data: dict) -> px.bar:
    """Bar chart plot of the age distributions based on the age brackets"""
    plot_data = {"bracket": list(data.keys()), "count": list(data.values())}

    fig = px.bar(plot_data, x="bracket", y="count", color="bracket",
                 labels={
                     "count": "Count",
                     "bracket": "Age Bracket"
                 },
                 title="Age Distribution"
                 )
    fig.update_layout(
        font=dict(
            size=18
        ),
        title_x=0.5
    )

    return fig


def mean_power_output(cut_off) -> float:
    """Extracts the mean total power of all rides in the past 12 hours and rounds it to 2 decimal places
    """
    sql = f"""SELECT AVG(total_power) FROM ride_details WHERE ride_details.started > '{cut_off}';"""
    data = query_executer(conn, sql)

    return round(list(data[0].values())[0], 2)


def total_power_output(cut_off) -> float:
    """Extracts the total power of all rides in the past 12 hours and rounds it to 2 decimal places
    """
    sql = f"""SELECT SUM(total_power) FROM ride_details WHERE ride_details.started > '{cut_off}';"""
    data = query_executer(conn, sql)

    return round(list(data[0].values())[0], 2)
