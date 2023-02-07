from kafka_consumer import *
from current_ride_utils import *


def read_in_from_kafka() -> dict:
    """Reads data from the Kafka consumer"""
    found_user = False
    ride_exists = False
    user_id = None
    heart_rate_abnormal = False
    heart_rate_counter = 0
    max_user_heart_rate = 0
    user_details = None
    c = kafka_consumer()
    current_ride_data = {
        "datetime": None, "duration": None, "current_resistance": 0,
        "current_heart_rate": 0, "current_rpm": 0, "current_power": 0,
        "max_resistance": 0, "max_rpm": 0, "max_power": 0,
        "total_power": 0
    }

    messages = get_kafka_messages(c)
    for message in messages:
        if "Getting user" in message:
            # resetting for new user
            found_user = False
            ride_exists = False
            current_ride_data = {
                "datetime": None, "duration": None, "current_resistance": 0,
                "current_heart_rate": 0, "current_rpm": 0, "current_power": 0,
                "max_resistance": 0, "max_rpm": 0, "max_power": 0,
                "total_power": 0
            }
            heart_rate_abnormal = False
            max_user_heart_rate = 0

        elif 'user_id' in message:
            # new user found
            found_user = True
            ride_exists = True
            user_details = extract_user_details(message)
            user_id = int(user_details["user_id"])
            user_age = age_from_dob(user_details["dob_date"])
            max_heart_rate = get_max_heart_rate(user_age)

        elif ("Ride - duration" in message):
            # get first part of data
            ride_duration_resistance = extract_ride_duration_resistance_data(
                message)

            current_ride_data["duration"] = float(
                ride_duration_resistance["duration"])
            current_ride_data["current_resistance"] = int(
                ride_duration_resistance["resistance"])
            current_ride_data["datetime"] = ride_duration_resistance["date_time"]

            if current_ride_data["max_resistance"] < int(ride_duration_resistance["resistance"]):
                current_ride_data["max_resistance"] = int(
                    ride_duration_resistance["resistance"])

        elif ("Telemetry - hrt" in message):
            # get second part of data
            ride_hrt_rpm_power = extract_ride_hrt_rpm_power(message)
            heart_rate = int(ride_hrt_rpm_power["heart_rate"])

            current_ride_data["current_heart_rate"] = heart_rate
            current_ride_data["current_rpm"] = int(ride_hrt_rpm_power["rpm"])
            current_ride_data["current_power"] = float(
                ride_hrt_rpm_power["power"])
            current_ride_data["total_power"] += float(
                ride_hrt_rpm_power["power"])

    return current_ride_data
