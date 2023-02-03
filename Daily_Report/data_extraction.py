from sqlwrapper import *
import datetime
import pandas as pd
import numpy as np

conn = get_db_connection()

TODAY = datetime.datetime.now()
TODAY_FORMATTED = datetime.datetime(TODAY.year, TODAY.month,
                                    TODAY.day, TODAY.hour, TODAY.minute, TODAY.second)
LAST_DAY = TODAY_FORMATTED - datetime.timedelta(days=1)


def extract_last_day(cut_off: datetime.datetime) -> pd.DataFrame:
    """Extracts all ride details from the previous 24 hours and stores the result in a Dataframe
    """
    sql = f"""SELECT * FROM ride_details WHERE started > '{cut_off}';"""
    data = query_executer(conn, sql)
    colNames = data[0].keys()

    return pd.DataFrame([[row[col] for col in colNames] for row in data], columns=colNames)


def extract_num_of_rides(df: pd.DataFrame) -> int:
    """Extracts the number of rides that occurred in the last 24 hours and returns an int
    """
    return df.shape[0]


# number of rides that day
# gender breakdown of riders
if __name__ == "__main__":
    df = extract_last_day(LAST_DAY)
    print(df.head())
    num_of_rides = extract_num_of_rides(df)
