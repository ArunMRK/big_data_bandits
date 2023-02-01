import ast
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
from typing import NoReturn
from sqlwrapper import *
from utils import *


def upload_user_details_to_db(details: dict) -> NoReturn:
    """Uploads given details into the user_details table"""
    sql = f"""INSERT INTO user_details (user_id, first, second, address, postcode, 
    dob_date, height, weight, gender, email, date_created, original_source, bike_serial)
    VALUES  ('{details['user_id']}', '{details['first']}', '{details['second']}', 
    '{details['address']}', '{details['postcode']}', '{details['dob_date']}', '{details['height']}','{details['weight']}', '{details['gender']}', '{details['email']}', 
    '{details['date_created']}', '{details['original_source']}', '{details['bike_serial']}');"""
    query_executer(conn ,sql)


def find_next_new_ride_id() -> int:
    """Returns the ride_id of the current/most recent ride"""
    sql = f"""SELECT ride_id FROM user_ride
        ORDER BY ride_id DESC
        LIMIT 1;"""
    result = query_executer(conn ,sql)

    for val in result:
        # need to extract the values from result and turn it into a list
        return list(val.values())[0]


def upload_ride_data_for_user_id(
        user_id: int, data: dict
    ) -> NoReturn:
    """Uploading the ride data to the data warehouse"""
    sql = f"""INSERT INTO ride_details (user_id, started, finished, duration, avg_rpm, avg_heart_rate, avg_power, avg_resistance, max_rpm, max_heart_rate, max_power, max_resistance) VALUES 
    ('{user_id}', '{data['started']}', '{data['finished']}', '{data['duration']}', '{data['avg_rpm']}', , '{data['avg_heart_rate']}', '{data['avg_power']}', '{data['avg_resistance']}','{data['max_rpm']}', '{data['max_heart_rate']}', '{data['max_power']}', '{data['max_resistance']}');"""
    query_executer(conn, sql)


def check_user_exists(user_id: int) -> bool:
    """Checks whether a user already exists in user_details"""
    sql = f"""SELECT * FROM user_details
        WHERE user_id ='{user_id}'"""
    result = query_executer(conn, sql)

    if result:
        return True

    return False


if __name__ == "__main__":
    load_dotenv(override=True, verbose=True)
    bootstrap_servers = os.getenv('BOOTSTRAP_SERVERS')
    security_protocol = 'SASL_SSL'
    sasl_username = os.getenv('SASL_USERNAME')
    sasl_password = os.getenv('SASL_PASSWORD')

    conn = get_db_connection()
    
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

    cont = True
    topic = 'deloton'

    c.subscribe([topic])

    # globals for kafka logic
    found_user = False
    user_id = None
    current_ride_data = {
        "datetime": [], "duration": [], "resistance": [], "heart_rate": [],
        "rpm": [], "power": []
        }
    ride_exists = False
    user_details = None

    print(f'Kafka set to run set to: {cont}, adjust `cont` to change')
    while cont:
        try:
            message = c.poll(1.0)
            if not message:
                print('None')
            else:
                print(current_ride_data)
                msg = message.value().decode()

                if 'beginning' in msg:
                    if ride_exists:
                        # TODO: if current ride data exists, we need to aggregate it and push it to the warehouse
                        if not check_user_exists(user_id):
                            upload_user_details_to_db(user_details)
                            date = extract_date(msg)

                    found_user = False
                    ride_exists = False
                    current_ride_data = {
                        "datetime": [], "duration": [], "resistance": [], 
                        "heart_rate": [], "rpm": [], "power": []
                        }
                    print('pass over message for new USER incoming')

                # (NEW USER ENTRY)
                elif 'user_id' in msg:
                    print("new user found")
                    # ** code for uploading user details to database **
                    found_user = True
                    user_details = extract_user_details(msg)
                    print(user_details)
                    user_id = user_details["user_id"]
                    ride_exists = True

                # (NEW DATA BUT NO CURRENTLY FOUND USER)
                elif 'user_id' not in msg and not found_user:
                    # *skip because caught mid-stream without user*
                    print('currently entered mid-stream, waiting for new user')

                # (USER IS FOUND, MSG is DATA)
                elif found_user and ('user_id' not in msg):
                    # get first parts of data
                    if 'Ride - duration' in msg:
                        ride_duration_resistance = extract_ride_duration_resistance_data(
                            msg)
                        current_ride_data["duration"].append(ride_duration_resistance["duration"])
                        current_ride_data["resistance"].append(ride_duration_resistance["resistance"])
                        current_ride_data["datetime"].append(ride_duration_resistance["date_time"])

                    elif 'Telemetry - hrt' in msg:
                        ride_hrt_rpm_power = extract_ride_hrt_rpm_power(msg)
                        current_ride_data["heart_rate"].append(ride_hrt_rpm_power["heart_rate"])
                        current_ride_data["rpm"].append(ride_hrt_rpm_power["rpm"])
                        current_ride_data["power"].append(ride_hrt_rpm_power["power"])
    
        except KeyboardInterrupt:
            c.close()