import base64
import datetime
import json
import time
import uuid
from dotenv import load_dotenv
from configparser import ConfigParser
import pandas as pd
import os
from confluent_kafka import Consumer, KafkaError, TopicPartition, KafkaException, Producer
import time
import datetime
import psycopg2
import psycopg2.extras

load_dotenv(override=True, verbose=True)

# Getting Data from Aurora RDBS AWS source
rds_db = os.getenv('RDS_DB_NAME')
rds_user = os.getenv('RDS_USER')
rds_password = os.getenv('RDS_PASSWORD')
rds_host = os.getenv('RDS_HOST')


def get_db_connection() :
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


print('TRYING DB CONNECTION\n')
conn = get_db_connection()
print('TRYING DB CONNECTION\n')

import ast


def split_name(name: str) -> list:
    """Split fullname into a first and second name. Returns a list where the first element is the first name and the second element is the last name
    """
    if name:
        return name.split(" ")
    else:
        return [None, None]


def unix_to_date(timestamp: int) -> datetime.date:
    """Take in unix timestamp (in ms, so have to divide by 1,000 to get seconds) and return date"""
    timestamp /= 1000
    time_and_date = datetime.datetime.fromtimestamp(
        timestamp)
    return time_and_date.date()


def extract_user_details(message: str) -> dict:
    """Extracts the user details and stores them in a dict"""
    data = ast.literal_eval(message)["log"]
    user_data = data.split("data = ")[1]
    raw_data = ast.literal_eval(user_data)

    name = split_name(raw_data["name"])
    dob_date = unix_to_date(raw_data["date_of_birth"])
    date_created = unix_to_date(raw_data["account_create_date"])
    full_address = raw_data["address"].split(",")
    postcode = full_address[-1]
    address = ", ".join(full_address[:-1])


    user_dict = {"user_id": raw_data["user_id"], "first": name[0],
        "second": name[1], "address": address, "postcode": postcode, 
        "dob_date": dob_date, "height": raw_data["height_cm"],
        "weight": raw_data["weight_kg"], "gender": raw_data["gender"], 
        "email": raw_data["email_address"], "date_created": date_created,
        "original_source": raw_data["original_source"],
        "bike_serial": raw_data["bike_serial"]}

    return user_dict


def upload_user_details_to_db(details):
    return


def get_id_from_database_for_made_user():
    return


def extract_duration_resistance_data(data):
    return


def extract_ride_hrt_rpm_power(data):
    return


def find_next_new_ride_id():
    return


def upload_ride_data_for_id(ride_id, ride_duration_resistance, ride_hrt_rpm_power):
    return


def combine_tables(ride_id, user_id, date):
    return


bootstrap_servers = os.getenv('BOOTSTRAP_SERVERS')
security_protocol = 'SASL_SSL'
sasl_username = os.getenv('SASL_USERNAME')
sasl_password = os.getenv('SASL_PASSWORD')

c = Consumer({
    'bootstrap.servers': bootstrap_servers,
    'group.id': f'deloton_stream' + str(uuid.uuid1()),
    'security.protocol': 'SASL_SSL',
    'sasl.mechanisms': 'PLAIN',
    'sasl.username': sasl_username,
    'sasl.password': sasl_password,
    'fetch.wait.max.ms': 6000,
    'auto.offset.reset': 'latest',
    'enable.auto.commit': 'false',
    'max.poll.interval.ms': '86400000',
    'topic.metadata.refresh.interval.ms': "-1",
    "client.id": 'id-002-005',
})
values = []
cont = True
topic = 'deloton'

c.subscribe([topic])

# globals for kafka logic
found_user = False
user_id = None
ride_id = None
ready_to_process = False

while cont == True:
    try:
        message = c.poll(1.0)
        if message is None:
            print('None')
        else:
            print(message.value().decode())

            msg = message.value().decode()

            if 'beginning' in msg['log']:
                print('pass over message for new USER incoming')

            # (NEW USER ENTRY)
            elif 'user_id' in msg['log']:

                found_user = True
                # ** code for uploading user details to database **
                user_details = extract_user_details(msg)
                upload_user_details_to_db(user_details)
                user_id = get_id_from_database_for_made_user()
                ride_id = None

            # (NEW DATA BUT NO CURRENTLY FOUND USER)
            elif 'user_id' not in msg['log'] and found_user == False:

                # *skip because caught mid-stream without user*
                print('currently entered mid-stream, waiting for new user')

            # (USER IS FOUND, MSG is DATA)
            elif (found_user == True) and ('user_id' not in msg['log']):

                # get first parts of data
                if 'Ride - duration' in msg['log']:
                    ride_duration_resistance = extract_duration_resistance_data(
                        msg)

                elif 'Telemetry - hrt' in msg['log']:
                    ride_hrt_rpm_power = extract_ride_hrt_rpm_power(msg['log'])
                    ready_to_process = True

                # (CHECK FOR NEW RIDE ESTABLISHED BY NEW USER INPUT)
                if ride_id == None and ready_to_process == True:
                    ride_id = find_next_new_ride_id()
                    upload_ride_data_for_id(
                        ride_id, ride_duration_resistance, ride_hrt_rpm_power)
                    combine_tables(ride_id, user_id, date)

                # (DATA FOR AN ALREADY ESTABLISHED RIDE)
                elif (ride_id is not None) and (ready_to_process == True):
                    upload_ride_data_for_id(
                        ride_id, ride_duration_resistance, ride_hrt_rpm_power)

    except KeyboardInterrupt:
        c.close()