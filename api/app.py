import psycopg2
import psycopg2.extras
from flask import Flask, current_app, jsonify, request
from flask_cors import CORS
from datetime import datetime
from sqlwrapper import *
from datetime import datetime, timedelta

# Set up
app = Flask(__name__)
CORS(app, origins=["http://127.0.0.1:5000"],  supports_credentials=True)
conn = get_db_connection()
ERROR_400 = 400
ACCEPTED_200 = 200

# Creates the index page


@app.route("/", methods=["GET"])
def index():
    return current_app.send_static_file("index.html")

# Get a ride with a specific ID


@app.route("/ride/<int:ride_id>", methods=["GET"])
def get_ride(ride_id):
    sql = f'SELECT * FROM ride_details where ride_id = {ride_id};'
    data = query_executer(conn, sql)
    if len(data) == 0:
        return '404: Ride does not exist: unable to show ride\'s details'
    return data

#  Get rider information (e.g. name, gender, age, avg. heart rate, number of rides)


@app.route("/rider/<int:user_id>", methods=["GET"])
def get_rider_information(user_id):
    sql = f'SELECT * FROM user_details where user_id = {user_id};'
    data = query_executer(conn, sql)
    if len(data) == 0:
        return '404: User does not exist: unable to show details'
    return data

#  Get all rides for a rider with a specific ID


@app.route("/rider/<int:user_id>/rides", methods=["GET"])
def get_rides_for_user(user_id):
    sql = f"""SELECT ride_id, started, finished, duration, avg_rpm, avg_heart_rate, avg_power, avg_resistance, max_rpm, max_heart_rate, max_power, max_resistance, total_power
              FROM ride_details as rd 
                    JOIN user_details as ud 
                        ON ud.user_id = rd.user_id 
                WHERE ud.user_id = {user_id};"""
    data = query_executer(conn, sql)
    if len(data) == 0:
        return '404: User does not exist: unable to show rides'
    return data

# Delete a with a specific ID


@app.route("/ride/<int:ride_id>/delete", methods=["GET"])
def delete_ride_for_id(ride_id):
    # show the ride to delete
    sql_get = f'SELECT * FROM ride_details where ride_id = {ride_id};'
    data = query_executer(conn, sql_get)
    # delete the ride
    sql_delete = f"""DELETE FROM ride_details WHERE ride_id = {ride_id};"""
    query_executer(conn, sql_delete)
    if len(data) == 0:
        return '404: Ride does not exist: Can\'t delete'
    return data


def get_date_and_latest(date):
    date = datetime.strptime(date, '%d-%m-%Y').date()
    tomorrow = datetime.strftime((date + timedelta(1)), '%Y-%m-%d')
    latest = datetime.strptime(tomorrow, '%Y-%m-%d') - timedelta(seconds=1)
    return [date, latest]

# get /daily or /daily?date=dd-mm-yyyy


@app.route("/daily", methods=["GET"])
def get_daily_for_given_date():
    chosen_date = request.args.get('date')

    # if /daily
    if chosen_date is None:
        todays_date = datetime.today().strftime('%d-%m-%Y')
        date_range = get_date_and_latest(todays_date)
        sql = f"""SELECT * FROM ride_details WHERE ( started > '{date_range[0]}' ) AND ( started < '{date_range[1]}' );"""
        data = query_executer(conn, sql)
        if len(data) == 0:
            return '404: No rides for given date: unable to show rides'
        return data

    # /daily?date=dd-mm-yyyy
    date_range = get_date_and_latest(chosen_date)
    sql = f"""SELECT * FROM ride_details WHERE ( started > '{date_range[0]}' ) AND ( started < '{date_range[1]}' );"""
    data = query_executer(conn, sql)
    if len(data) == 0:
        return '404: No rides for given date: unable to show rides'
    return data
