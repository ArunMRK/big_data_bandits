from kafka_consumer import *
from current_ride_utils import *
import pprint

def read_in_from_kafka():

    # if found_details == None:
    #     return
    print('Started read_in_fom_kafka')
    found_user = False
    ride_exists = False
    user_id = None
    heart_rate_abnormal=False
    heart_rate_counter = 0
    max_user_heart_rate = 0
    user_details = None
    c = kafka_consumer()
    current_ride_data = {
                "datetime": None, "duration": None, "current_resistance": 0,
                "current_heart_rate": 0, "current_rpm": 0, "current_power": 0,
                "max_resistance": 0,"max_rpm": 0, "max_power": 0,
                "total_power": 0
            }
    
    messages = get_kafka_messages(c)
    print('Kafka reader line 25')
    for message in messages:
        print(message)
        print('Kafka reader line 29')
        if "Getting user" in message:
            ''' Resetting variables for new user'''
            found_user = False
            ride_exists = False
            current_ride_data = {
                "datetime": None, "duration": None, "current_resistance": 0,
                "current_heart_rate": 0, "current_rpm": 0, "current_power": 0,
                "max_resistance": 0,"max_rpm": 0, "max_power": 0,
                "total_power": 0
            }
            heart_rate_abnormal=False
            max_user_heart_rate = 0

        elif 'user_id' in message:
            '''New user found'''
            print('Kafka reader line 45')
            found_user = True
            ride_exists = True
            user_details = extract_user_details(message)
            user_id = int(user_details["user_id"])
            user_age = age_from_dob(user_details["dob_date"])
            max_heart_rate = get_max_heart_rate(user_age)

        # elif found_user and ("Ride - duration" in message):
        elif  ("Ride - duration" in message):
            ''' get first part of data if user exists'''
            print('Kafka reader line 56')
            ride_duration_resistance = extract_ride_duration_resistance_data(
                message)

            current_ride_data["duration"] = float(ride_duration_resistance["duration"])
            current_ride_data["current_resistance"] = int(ride_duration_resistance["resistance"])
            current_ride_data["datetime"]= ride_duration_resistance["date_time"]

            if current_ride_data["max_resistance"] < int(ride_duration_resistance["resistance"]):
                current_ride_data["max_resistance"] = int(ride_duration_resistance["resistance"])
                
        # elif found_user and ("Telemetry - hrt" in message):
        elif ("Telemetry - hrt" in message):
            print('Kafka reader line 69')
            '''  get second part of data if user exists'''
            ride_hrt_rpm_power = extract_ride_hrt_rpm_power(message)
            heart_rate = int(ride_hrt_rpm_power["heart_rate"])
            print('line 73')
            # if (heart_rate > max_heart_rate):
            #     '''Trigger that checks the heart rate'''
            #     heart_rate_abnormal=True

            print('line 78')
            current_ride_data["current_heart_rate"] = heart_rate
            current_ride_data["current_rpm"] = int(ride_hrt_rpm_power["rpm"])
            current_ride_data["current_power"] = float(ride_hrt_rpm_power["power"])
            current_ride_data["total_power"] += float(ride_hrt_rpm_power["power"])
            print('line 83')
            # if current_ride_data["max_rpm"] < int(ride_duration_resistance["rpm"]):
            #     current_ride_data["max_rpm"] = int(ride_duration_resistance["rpm"])
            # if current_ride_data["max_power"] < int(ride_duration_resistance["power"]):
            #     current_ride_data["max_power"] = int(ride_duration_resistance["power"])
            print('line 88')
        
    # print('reached 1')
    # print(current_ride_data)
    print(current_ride_data)
    print('Kafka reader line 92')
    # print(user_details)
    # print('reached 2')
    return current_ride_data