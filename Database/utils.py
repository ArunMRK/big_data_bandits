import re
import datetime
import ast
from statistics import mean
from datetime import date
from typing import NoReturn
import json
import boto3


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
    """Take in unix timestamp (in ms, so have to divide by 1,000 to get seconds) and return date
    """
    timestamp /= 1000
    time_and_date = datetime.datetime.fromtimestamp(timestamp)

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

    # need to escape all ' when adding data to a database using sql
    user_dict = {"user_id": raw_data["user_id"], "first": name[0].replace("'", "''"),
                 "second": name[1].replace("'", "''"), "address": address.replace("'", "''"), "postcode": postcode,
                 "dob_date": dob_date, "height": raw_data["height_cm"],
                 "weight": raw_data["weight_kg"], "gender": raw_data["gender"],
                 "email": raw_data["email_address"].replace("'", "''"), "date_created": date_created,
                 "original_source": raw_data["original_source"].replace("'", "''"),
                 "bike_serial": raw_data["bike_serial"]}

    return user_dict


def extract_date(message: str) -> datetime.time:
    """Extracts the date from the kafka data"""
    regex = "[0-9]{4}(-[0-9]{2}){2}"
    result = re.search(regex, message).group(0)
    date = datetime.datetime.strptime(result, "%Y-%m-%d").date()

    return date


def extract_date_time(message: str) -> datetime.datetime:
    """Extracts the date from the kafka data"""
    regex = "[0-9]{4}(-[0-9]{2}){2} [0-9]{2}:[0-9]{2}:[0-9]{2}"
    result = re.search(regex, message).group(0)
    date = datetime.datetime.strptime(result, "%Y-%m-%d %H:%M:%S")

    return date


def extract_ride_duration_resistance_data(message: str) -> dict:
    """Extracting the Duration-Resistance data from log"""
    words = {"Ride - duration": "duration", "resistance": "resistance"}
    test = str(message)
    data = ast.literal_eval(test)["log"].split("[INFO]: ")[-1]
    data_array = data.strip().split(";")
    date_time = extract_date_time(message)

    message_dict = {words[val.split("= ")[0].strip()]: val.split(
        "= ")[-1] for val in data_array}
    ride_dict = {"duration": message_dict["duration"],
                 "resistance": message_dict["resistance"], "date_time": date_time}

    return ride_dict


def extract_ride_hrt_rpm_power(message: str) -> dict:
    """Extracting the hrt, rpm, power data from the log"""
    words = {"Telemetry - hrt": "heart_rate", "rpm": "rpm", "power": "power"}
    data = ast.literal_eval(message)["log"].split("[INFO]: ")[-1]
    message_arr = data.strip().split(";")
    message_dict = {words[val.split("= ")[0].strip()]: val.split(
        "= ")[-1] for val in message_arr}

    ride_dict = {"heart_rate": message_dict["heart_rate"],
                 "rpm": message_dict["rpm"], "power": message_dict["power"]}

    return ride_dict


def current_ride_summary(current_ride_data: list) -> dict:
    """Takes in readings over a ride and returns the aggregate values for rpm, heart rate, power and resistance over the course of the ride; also includes the start and end times of the ride and total duration
    """
    heart_readings = current_ride_data["heart_rate"]
    power_readings = current_ride_data["power"]
    rpm_readings = current_ride_data["rpm"]
    resistance_readings = current_ride_data["resistance"]
    duration_readings = current_ride_data["duration"]
    datetime_readings = current_ride_data["datetime"]

    data_dict = {
        "avg_rpm": mean(rpm_readings),
        "avg_heart_rate": mean(heart_readings),
        "avg_power": mean(power_readings),
        "avg_resistance": mean(resistance_readings),
        "max_rpm": max(rpm_readings),
        "max_heart_rate": max(heart_readings),
        "max_power": max(power_readings),
        "max_resistance": max(resistance_readings),
        "total_power": sum(power_readings),
        "started": datetime_readings[0],
        "finished": datetime_readings[-1],
        "duration": duration_readings[-1]
    }

    return data_dict


def get_max_heart_rate(age: int) -> int:
    """Determines the maximum working heart rate given the users age."""
    return 220 - age + 10


def age_from_dob(born: datetime.date) -> int:
    """Find user's age from DOB"""
    today = date.today()

    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def dump_user_data_to_s3(user_data: dict) -> NoReturn:
    """Dumps the current user details to an S3 bucket - this includes the name, gender, age, height, weight and maximum allowed heart rate
    """
    s3 = boto3.resource("s3")
    json_user_data = json.dumps(user_data)
    object = s3.Object("big-data-bandits", "current-user/user-data.json")
    object.put(Body=json_user_data)
