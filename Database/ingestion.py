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
import re
from typing import NoReturn
from sqlwrapper import *



load_dotenv(override=True, verbose=True)

conn = get_db_connection()

def split_name(name: str) -> list:
    """Split fullname into a first and second name. Returns a list where the first element is the first name and the second element is the last name
    """
    exceptions = ["Mr", "Mrs", "Miss", "Dr", "Mx", "Prof", "Ms",
                  "Mr.", "Mrs.", "Miss.", "Dr.", "Mx.", "Prof.", "Ms."]

    if name:
        split_name = name.split(" ")
        if split_name[0] in exceptions:
            return [split_name[1], split_name[-1]]
        return [split_name[0], split_name[-1]]
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


def extract_date(message: str) -> datetime.time:
    """Extracts the date from the kafka data"""
    regex = "[0-9]{4}(-[0-9]{2}){2}"
    result = re.search(regex, message).group(0)
    date = datetime.datetime.strptime(result, '%Y-%m-%d').date()
    print(date)
    return date


def extract_date_time(message: str) -> datetime.time:
    """Extracts the date from the kafka data"""
    regex = "[0-9]{4}(-[0-9]{2}){2} [0-9]{2}:[0-9]{2}:[0-9]{2}"
    result = re.search(regex, message).group(0)
    date = datetime.datetime.strptime(result, '%Y-%m-%d %H:%M:%S')
    print(type(date))
    return date


def upload_user_details_to_db(details: dict) -> NoReturn:
    """Uploads given details into the user_details table"""
    sql = f"""INSERT INTO user_details (user_id, first, second, address, postcode, 
    dob_date, height, weight, gender, email, date_created, original_source, bike_serial)
    VALUES  ('{details['user_id']}', '{details['first']}', '{details['second']}', 
    '{details['address']}', '{details['postcode']}', '{details['dob_date']}', '{details['height']}','{details['weight']}', '{details['gender']}', '{details['email']}', 
    '{details['date_created']}', '{details['original_source']}', '{details['bike_serial']}');"""
    query_executer(conn ,sql)


def extract_ride_duration_resistance_data(message: str):
    """Extracting the Duration-Resistance data from log"""
    words = {"Ride - duration": "duration", "resistance": "resistance"}
    test = str(message)
    data = ast.literal_eval(test)["log"].split("[INFO]: ")[-1]
    data_array = data.strip().split(";")
    date_time = extract_date_time(message)
    message_dict = {words[val.split("= ")[0].strip()]: val.split(
        "= ")[-1] for val in data_array}
    ride_dict = {'duration': message_dict['duration'],
                 'resistance': message_dict['resistance'], 'date_time': date_time}

    return ride_dict


def extract_ride_hrt_rpm_power(message: str):
    words = {"Telemetry - hrt": "heart_rate", "rpm": "rpm", "power": "power"}
    data = ast.literal_eval(message)["log"].split("[INFO]: ")[-1]
    message_arr = data.strip().split(";")
    message_dict = {words[val.split("= ")[0].strip()]: val.split(
        "= ")[-1] for val in message_arr}

    ride_dict = {'heart_rate': message_dict['heart_rate'],
                 'rpm': message_dict['rpm'], 'power': message_dict['power']}

    return ride_dict


def find_next_new_ride_id() -> int:
    """Returns the ride_id of the current/most recent ride"""
    sql = f"""SELECT ride_id FROM user_ride
        ORDER BY ride_id DESC
        LIMIT 1;"""
    result = query_executer(conn ,sql)

    for val in result:
        # need to extract the values from result and turn it into a list
        return list(val.values())[0]


def upload_ride_data_for_id(
    ride_id: int, ride_duration_resistance: dict, ride_hrt_rpm_power: dict
) -> NoReturn:
    sql = f"""INSERT INTO ride_details (ride_id, duration, date_time, resistance, heart_rate,
    rpm, power) 
    VALUES 
    ('{ride_id}', '{ride_duration_resistance['duration']}', 
    '{ride_duration_resistance['date_time']}', 
    '{ride_duration_resistance['resistance']}', '{ride_hrt_rpm_power['heart_rate']}',
    '{ride_hrt_rpm_power['rpm']}', '{ride_hrt_rpm_power['power']}');"""
    query_executer(conn, sql)


def combine_tables(user_id: int, date: datetime.time) -> NoReturn:
    """Function that executes code for adding data to the joining middle table user_ride"""
    sql = f"""INSERT INTO user_ride (user_id, date) VALUES
        ('{user_id}', '{date}')"""
    query_executer(conn, sql)


def check_user_exists(user_id: int) -> bool:
    """Checks whether a user already exists in user_details"""
    sql = f"""SELECT * FROM user_details
        WHERE user_id ='{user_id}'"""
    result = query_executer(conn, sql)

    if result:
        return True

    return False


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

print(f'Kafka set to run set to: {cont}, adjust `cont` to change')
while cont:
    try:
        message = c.poll(1.0)
        if not message:
            print('None')
        else:
            msg = message.value().decode()
            print(msg)

            if 'beginning' in msg:
                found_user = False
                user_id = None
                ride_id = None
                ready_to_process = False
                print('pass over message for new USER incoming')

            # (NEW USER ENTRY)
            elif 'user_id' in msg:
                print("new user found")
                # ** code for uploading user details to database **
                found_user = True
                user_details = extract_user_details(msg)
                user_id = user_details["user_id"]

                if not check_user_exists(user_id):
                    upload_user_details_to_db(user_details)
                    date = extract_date(msg)
                    combine_tables(user_id, date)
                    ride_id = find_next_new_ride_id()

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

                elif 'Telemetry - hrt' in msg:
                    ride_hrt_rpm_power = extract_ride_hrt_rpm_power(msg)
                    ready_to_process = True

                # (CHECK FOR NEW RIDE ESTABLISHED BY NEW USER INPUT)
                if ready_to_process:
                    print("adding row to database")
                    upload_ride_data_for_id(
                        ride_id, ride_duration_resistance, ride_hrt_rpm_power)
                    ready_to_process = False

    except KeyboardInterrupt:
        c.close()