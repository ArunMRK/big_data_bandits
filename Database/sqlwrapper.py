import psycopg2
import psycopg2.extras
import os
from dotenv import load_dotenv
from typing import NoReturn

load_dotenv(override=True, verbose=True)

# Getting Data from Aurora RDBS AWS source
rds_db = os.getenv('RDS_DB_NAME')
rds_user = os.getenv('RDS_USER')
rds_password = os.getenv('RDS_PASSWORD')
rds_host = os.getenv('RDS_HOST')


def get_db_connection() -> psycopg2.extensions.connection:
    """ Create a connection for database postgres Aurora"""
    try:
        conn = psycopg2.connect(f"""
    dbname={rds_db}
    user={rds_user} 
    password={rds_password}
    host={rds_host}""")
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
                print("Executing query - no result to return")
    else:
        return "No connection"


def upload_user_details_to_db(
    conn: psycopg2.extensions.connection, details: dict
) -> NoReturn:
    """Uploads given details into the user_details table"""
    sql = f"""INSERT INTO user_details (user_id, first, second, address, postcode, 
    dob_date, height, weight, gender, email, date_created, original_source, bike_serial)
    VALUES  ('{details['user_id']}', '{details['first']}', '{details['second']}', 
    '{details['address']}', '{details['postcode']}', '{details['dob_date']}', '{details['height']}','{details['weight']}', '{details['gender']}', '{details['email']}', 
    '{details['date_created']}', '{details['original_source']}', '{details['bike_serial']}');"""
    query_executer(conn, sql)


def upload_ride_data_for_user_id(
    conn: psycopg2.extensions.connection, user_id: int, data: dict
) -> NoReturn:
    """Uploading the ride data to the data warehouse"""
    sql = f"""INSERT INTO ride_details (user_id, started, finished, duration, avg_rpm, avg_heart_rate, avg_power, avg_resistance, max_rpm, max_heart_rate, max_power, max_resistance, total_power) VALUES 
    ('{user_id}', '{data['started']}', '{data['finished']}', '{data['duration']}', '{data['avg_rpm']}', '{data['avg_heart_rate']}', '{data['avg_power']}', '{data['avg_resistance']}', '{data['max_rpm']}', '{data['max_heart_rate']}', '{data['max_power']}', '{data['max_resistance']}', '{data['total_power']}');"""
    query_executer(conn, sql)


def check_user_exists(
    conn: psycopg2.extensions.connection, user_id: int
) -> bool:
    """Checks whether a user already exists in user_details"""
    sql = f"""SELECT * FROM user_details
        WHERE user_id ='{user_id}'"""
    result = query_executer(conn, sql)

    if result:
        return True

    return False
