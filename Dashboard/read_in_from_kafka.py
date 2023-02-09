from kafka_consumer import *
from current_ride_utils import *
def read_in_from_kafka(consumer: Consumer) -> dict:
    """Reads data from the Kafka consumer"""
    user_details = None
    current_ride_data = {
        "datetime": None, "duration": None, "current_resistance": 0,
        "current_heart_rate": 0, "current_rpm": 0, "current_power": 0,
        "max_resistance": 0, "max_rpm": 0, "max_power": 0,
        "total_power": 0
    }
    messages = get_kafka_messages(consumer)
    for message in messages:
        if "Getting user" in message:
            # resetting user_details for new user
            current_ride_data = {
                "datetime": None, "duration": None, "current_resistance": 0,
                "current_heart_rate": 0, "current_rpm": 0, "current_power": 0,
                "max_resistance": 0, "max_rpm": 0, "max_power": 0,
                "total_power": 0
            }
        elif "user_id" in message:
            # new user found
            print("FOUND USER")
            user_details = extract_user_details(message)
        elif ("Ride - duration" in message):
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
            ride_hrt_rpm_power = extract_ride_hrt_rpm_power(message)
            heart_rate = int(ride_hrt_rpm_power["heart_rate"])
            current_ride_data["current_heart_rate"] = heart_rate
            current_ride_data["current_rpm"] = int(ride_hrt_rpm_power["rpm"])
            current_ride_data["current_power"] = float(
                ride_hrt_rpm_power["power"])
            current_ride_data["total_power"] += float(
                ride_hrt_rpm_power["power"])
    
    # print(current_ride_data)
    # print(user_details)
    return current_ride_data, user_details