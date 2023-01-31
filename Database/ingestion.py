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

load_dotenv(override=True, verbose=True)

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


while cont == True:
    try:
        message = c.poll(1.0)
        if message is None:
            print('None')
        else:
            print(message.value().decode())

            # msg = message.value().decode()
            
            # (NEW USER ENTRY)
            # if 'User' IN msg :
                
                # found_user == True
                # ** code for uploading user details to database **
                # user_details = e
                # user_id = get_id_from_database_for_made_user()
                # ride_id = None
            
            # (NEW DATA BUT NO CURRENTLY FOUND USER)
            # elif 'User' NOT IN msg AND found_user == False:

                # *skip because caught mid-stream without user*

            # (USER IS FOUND, MSG is DATA)
            # elif found_user == True AND 'User' NOT IN msg :

                # (CHECK FOR CURRENT RIDE)
                # if ride_id = None:
                    # ride_id = find_next_new_ride_id()
                    # upload_ride_data_for_id(ride_id)

                # (DATA FOR AN ALREADY ESTABLISHED RIDE)
                # if ride_id IS NOT None:
                    # upload_ride_data_for_id(ride_id)


    except KeyboardInterrupt:
        c.close()


def split_name(name: str) -> list:
    """Split fullname into a first and second name. Returns a list where the first element is the first name and the second element is the last name
    """
    if name:
        return name.split(" ")
    else:
        return [None, None]
