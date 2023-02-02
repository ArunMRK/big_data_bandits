from utils import *
from sqlwrapper import *
from Heart_Rate.heart_rate_script import *
from kafka_consumer import *

conn = get_db_connection()

if __name__ == "__main__":
    c = kafka_consumer()

    found_user = False
    user_id = None
    ride_exists = False
    user_details = None
    max_heart_rate = 0
    current_ride_data = {
        "datetime": [], "duration": [], "resistance": [], "heart_rate": [],
        "rpm": [], "power": []
    }
    heart_rate_counter = 0
    max_user_heart_rate = 0
    notification_sent = True  # turn back to false when I can send emails again

    while True:
        message = get_kafka_message(c)

        if message:
            if "Getting user" in message:
                # if a ride and user exists, adds data to data warehouse
                if ride_exists and found_user:
                    # checking whether a user with an id already exists
                    if not check_user_exists(conn, user_id):
                        upload_user_details_to_db(conn, user_details)

                    print("Loading data to data warehouse...")
                    current_ride_details = current_ride_summary(
                        current_ride_data)
                    upload_ride_data_for_user_id(
                        conn, user_id, current_ride_details)

                # resetting variables
                found_user = False
                ride_exists = False
                max_heart_rate = 0
                current_ride_data = {
                    "datetime": [], "duration": [], "resistance": [],
                    "heart_rate": [], "rpm": [], "power": []
                }
                heart_rate_counter = 0
                max_user_heart_rate = 0
                notification_sent = False

            # new user found block
            elif 'user_id' in message:
                print("New user found in stream...")
                found_user = True
                ride_exists = True

                user_details = extract_user_details(message)
                user_id = int(user_details["user_id"])
                user_age = age_from_dob(user_details["dob_date"])
                max_heart_rate = get_max_heart_rate(user_age)

            # get first part of data if user exists
            elif found_user and ("Ride - duration" in message):
                ride_duration_resistance = extract_ride_duration_resistance_data(
                    message)

                current_ride_data["duration"].append(
                    float(ride_duration_resistance["duration"]))
                current_ride_data["resistance"].append(
                    int(ride_duration_resistance["resistance"]))
                current_ride_data["datetime"].append(
                    ride_duration_resistance["date_time"])

            # get second part of data if user exists
            elif found_user and ("Telemetry - hrt" in message):
                ride_hrt_rpm_power = extract_ride_hrt_rpm_power(message)
                heart_rate = int(ride_hrt_rpm_power["heart_rate"])

                # trigger that checks the heart rate
                if (heart_rate > max_heart_rate) and not notification_sent:
                    heart_rate_counter += 1

                    if heart_rate > max_user_heart_rate:
                        max_user_heart_rate = heart_rate

                    if heart_rate_counter >= 5:
                        # sends email if heart rate is dangerous
                        user_alert_data = get_user_details(
                            user_age, user_details["first"], user_details["second"], max_user_heart_rate, max_heart_rate, ride_duration_resistance["date_time"])
                        email_alert(user_alert_data)
                        notification_sent = True

                current_ride_data["heart_rate"].append(heart_rate)
                current_ride_data["rpm"].append(int(ride_hrt_rpm_power["rpm"]))
                current_ride_data["power"].append(
                    float(ride_hrt_rpm_power["power"]))
