from sqlwrapper import *
import datetime
import pandas as pd
import numpy as np
import csv
import plotly.express as px

conn = get_db_connection()

TODAY = datetime.datetime.now()
TODAY_FORMATTED = datetime.datetime(TODAY.year, TODAY.month,
                                    TODAY.day, TODAY.hour, TODAY.minute, TODAY.second)
LAST_DAY = TODAY_FORMATTED - datetime.timedelta(days=1)


def extract_last_day_data(cut_off: datetime.datetime) -> pd.DataFrame:
    """Extracts all ride details from the previous 24 hours and stores the result in a Dataframe
    """
    sql = f"""SELECT * FROM ride_details WHERE started > '{cut_off}';"""
    data = query_executer(conn, sql)
    colNames = data[0].keys()
    last_day_rides = pd.DataFrame(
        [[row[col] for col in colNames] for row in data], columns=colNames)

    return last_day_rides


def extract_last_day_users(df: pd.DataFrame) -> pd.DataFrame:
    """Determines the unique riders and extracts all information about them into a Dataframe
    """
    user_ids = tuple(df["user_id"].unique())

    sql = f"""SELECT * FROM user_details WHERE user_id IN {user_ids}"""
    data = query_executer(conn, sql)
    colNames = data[0].keys()
    last_day_users = pd.DataFrame(
        [[row[col] for col in colNames] for row in data], columns=colNames)

    return last_day_users


def gender_distribution(df: pd.DataFrame) -> dict:
    """Determines the gender distribution of riders for the past 24 hours; returns a dict
    """
    data = dict(df["gender"].value_counts())

    return data


def gender_plot(data: dict) -> px.pie:
    """Pie plot of the gender distributions for the riders for the past 24 hours
    """
    plot_data = {"gender": list(data.keys()), "count": list(data.values())}

    fig = px.pie(
        plot_data, values="count", names="gender",
        labels={
            "count": "Count",
            "gender": "Gender"
        }, title=f"Gender Distribution ({LAST_DAY} to {TODAY_FORMATTED})"
    )

    return fig.write_image("/tmp/gender_distribution.jpg")


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

    fig = px.bar(plot_data, x="bracket", y="count",
                 labels={
                     "count": "Count",
                     "bracket": "Age Bracket"
                 },
                 title=f"Age Distribution ({LAST_DAY} to {TODAY_FORMATTED})"
                 )

    return fig.write_image("/tmp/age_distribution.jpg")


def extract_averages(df: pd.DataFrame) -> dict:
    """Extracts the average duration, rpm, power, resistance, heart rate from the last 24 hours of data - returns a dict"""
    avg_data = {
        "avg_duration": df["duration"].mean(),
        "avg_rpm": df["avg_rpm"].mean(),
        "avg_power": df["avg_power"].mean(),
        "avg_resistance": df["avg_resistance"].mean(),
        "avg_heart_rate": df["avg_heart_rate"].mean()
    }

    return avg_data


def extract_total(df: pd.DataFrame) -> dict:
    """Extracts total duration and power for the past 24 hours - returns a dict
    """
    total_data = {
        "total_duration": df["duration"].sum(),
        "total_power": df["total_power"].sum()
    }

    return total_data
