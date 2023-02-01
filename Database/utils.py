import re
import datetime
import ast

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


def extract_ride_duration_resistance_data(message: str) -> dict:
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


def extract_ride_hrt_rpm_power(message: str) -> dict:
    """Extracting the hrt, rpm, power data from the log"""
    words = {"Telemetry - hrt": "heart_rate", "rpm": "rpm", "power": "power"}
    data = ast.literal_eval(message)["log"].split("[INFO]: ")[-1]
    message_arr = data.strip().split(";")
    message_dict = {words[val.split("= ")[0].strip()]: val.split(
        "= ")[-1] for val in message_arr}

    ride_dict = {'heart_rate': message_dict['heart_rate'],
                 'rpm': message_dict['rpm'], 'power': message_dict['power']}

    return ride_dict