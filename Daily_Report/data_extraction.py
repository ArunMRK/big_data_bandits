from sqlwrapper import *
import datetime
import pandas as pd
import numpy as np
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
    plot_data = {"gender": list(data.keys()), "count": list(data.values())}

    return plot_data


def gender_plot(data: dict) -> px.pie:
    """Pie plot of the gender distributions for the riders for the past 24 hours
    """
    fig = px.pie(
        data, values="count", names="gender",
        labels={
            "count": "Count",
            "gender": "Gender"
        }, title=f"Gender Distribution ({LAST_DAY} to {TODAY_FORMATTED})"
    )

    return fig.write_image("Plots/gender_distribution.png")


if __name__ == "__main__":
    rides = extract_last_day_data(LAST_DAY)
    print(rides.head())
    num_of_rides = rides.shape[0]
    print(num_of_rides)
    users = extract_last_day_users(rides)
    print(users)
    genders = gender_distribution(users)
    print(genders)
    gender_plot(genders)
