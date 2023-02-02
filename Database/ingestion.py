import ast
import base64
import datetime
import json
import time
import uuid
import boto3
import pandas as pd
import os
from dotenv import load_dotenv
from configparser import ConfigParser
from confluent_kafka import Consumer, KafkaError, TopicPartition, KafkaException, Producer
from typing import NoReturn
from sqlwrapper import *
from utils import *
from s3_connection import *

load_dotenv(override=True, verbose=True)
BOOTSTRAP_SERVERS = os.getenv('BOOTSTRAP_SERVERS')
SASL_USERNAME = os.getenv('SASL_USERNAME')
SASL_PASSWORD = os.getenv('SASL_PASSWORD')
s3 = boto3.client("s3")
conn = get_db_connection()


def kafka_consumer() -> Consumer:
    """Makes a connection to a Kafka consumer"""
    c = Consumer({
        'bootstrap.servers': BOOTSTRAP_SERVERS,
        'group.id': f'deloton_stream' + str(uuid.uuid1()),
        'security.protocol': 'SASL_SSL',
        'sasl.mechanisms': 'PLAIN',
        'sasl.username': SASL_USERNAME,
        'sasl.password': SASL_PASSWORD,
        'fetch.wait.max.ms': 6000,
        'auto.offset.reset': 'latest',
        'enable.auto.commit': 'false',
        'max.poll.interval.ms': '86400000',
        'topic.metadata.refresh.interval.ms': "-1",
        "client.id": 'id-002-005',
    })
    c.subscribe(["deloton"])

    return c


def get_kafka_message(consumer: Consumer) -> str:
    """Gets the latest log from a Kafka consumer"""
    message = consumer.poll(1.0)

    if message:
        return message.value().decode()


def upload_user_details_to_db(details: dict) -> NoReturn:
    """Uploads given details into the user_details table"""
    sql = f"""INSERT INTO user_details (user_id, first, second, address, postcode, 
    dob_date, height, weight, gender, email, date_created, original_source, bike_serial)
    VALUES  ('{details['user_id']}', '{details['first']}', '{details['second']}', 
    '{details['address']}', '{details['postcode']}', '{details['dob_date']}', '{details['height']}','{details['weight']}', '{details['gender']}', '{details['email']}', 
    '{details['date_created']}', '{details['original_source']}', '{details['bike_serial']}');"""
    query_executer(conn, sql)


def upload_ride_data_for_user_id(
    user_id: int, data: dict
) -> NoReturn:
    """Uploading the ride data to the data warehouse"""
    sql = f"""INSERT INTO ride_details (user_id, started, finished, duration, avg_rpm, avg_heart_rate, avg_power, avg_resistance, max_rpm, max_heart_rate, max_power, max_resistance, total_power) VALUES 
    ('{user_id}', '{data['started']}', '{data['finished']}', '{data['duration']}', '{data['avg_rpm']}', '{data['avg_heart_rate']}', '{data['avg_power']}', '{data['avg_resistance']}', '{data['max_rpm']}', '{data['max_heart_rate']}', '{data['max_power']}', '{data['max_resistance']}', '{data['total_power']}');"""
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
    c = kafka_consumer()

    found_user = False
    user_id = None
    ride_exists = False
    user_details = None
    current_ride_data = {
        "datetime": [], "duration": [], "resistance": [], "heart_rate": [],
        "rpm": [], "power": []
    }

    cont = True  # for test
    # for test
    print(f'Kafka set to run set to: {cont}, adjust `cont` to change')
    while cont:
        try:
            message = get_kafka_message(c)

            if message:
                print(message)  # for test

                if "Getting user" in message:
                    if ride_exists and found_user:
                        if not check_user_exists(user_id):
                            upload_user_details_to_db(user_details)

                        current_ride_details = current_ride_summary(
                            current_ride_data)

                        upload_ride_data_for_user_id(
                            user_id, current_ride_details)

                    found_user = False
                    ride_exists = False
                    current_ride_data = {
                        "datetime": [], "duration": [], "resistance": [],
                        "heart_rate": [], "rpm": [], "power": []
                    }

                # (NEW USER ENTRY)
                elif 'user_id' in message:
                    print("new user found")  # for test
                    # ** code for uploading user details to database **
                    found_user = True
                    ride_exists = True
                    user_details = extract_user_details(message)
                    user_id = int(user_details["user_id"])
                    user_age = age_from_dob(user_details['dob_date'])
                    ride_exists = True

                # (NEW DATA BUT NO CURRENTLY FOUND USER)
                elif 'user_id' not in message and not found_user:
                    # *skip because caught mid-stream without user*
                    # for test
                    print('currently entered mid-stream, waiting for new user')

                # (USER IS FOUND, MSG is DATA)
                elif found_user and ('user_id' not in message):
                    # get first parts of data
                    if 'Ride - duration' in message:
                        ride_duration_resistance = extract_ride_duration_resistance_data(
                            message)
                        current_ride_data["duration"].append(
                            float(ride_duration_resistance["duration"]))
                        current_ride_data["resistance"].append(
                            int(ride_duration_resistance["resistance"]))
                        current_ride_data["datetime"].append(
                            ride_duration_resistance["date_time"])

                    elif 'Telemetry - hrt' in message:
                        ride_hrt_rpm_power = extract_ride_hrt_rpm_power(
                            message)
                        current_ride_data["heart_rate"].append(
                            int(ride_hrt_rpm_power["heart_rate"]))
                        current_ride_data["rpm"].append(
                            int(ride_hrt_rpm_power["rpm"]))
                        current_ride_data["power"].append(
                            float(ride_hrt_rpm_power["power"]))

        except KeyboardInterrupt:
            c.close()
