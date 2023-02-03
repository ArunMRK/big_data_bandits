import psycopg2
import psycopg2.extras
from flask import Flask, current_app, jsonify, request
from flask_cors import CORS
from datetime import datetime
from sqlwrapper import *


#Set up
app = Flask(__name__)
CORS(app, origins=["http://127.0.0.1:5000"],  supports_credentials=True)
conn = get_db_connection()
ERROR_400 = 400
ACCEPTED_200 = 200

# Creates the index page
@app.route("/", methods=["GET"])
def index():
    return current_app.send_static_file("index.html")

#Get a ride with a specific ID
@app.route("/ride/<int:id>", methods=["GET"])
def get_ride():
    return

#  Get rider information (e.g. name, gender, age, avg. heart rate, number of rides)
@app.route("/rider/<str:user_id>", methods=["GET"])
def get_rider_information():
    return

#  Get all rides for a rider with a specific ID
@app.route("/rider/<str:user_id>/rides", methods=["GET"])
def get_rides_for_user():
    return

# Delete a with a specific ID
@app.route("/ride/:id", methods=["DELETE"])
def delete_ride_for_id():
    return

# Get all of the rides in the current day
@app.route("/daily", methods=["GET"])
def get_daily():
    return

# Get all rides for a specific date
# GET /daily?date=01-01-2020
@app.route("/daily", methods=["GET"])
def get_daily_for_given_date():
    # potentially more than 1 date given
    args = request.args["tags"].split(',')
    return

