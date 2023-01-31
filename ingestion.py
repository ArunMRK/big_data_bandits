import base64
import datetime
import json
import time
import uuid
from dotenv import load_dotenv
from configparser import ConfigParser
import pandas as pd
from confluent_kafka import Consumer, KafkaError, TopicPartition, KafkaException, Producer

load_dotenv(override=True,verbose=True)
import os

bootstrap_servers=os.getenv('BOOTSTRAP_SERVERS')
security_protocol='SASL_SSL'
sasl_username=os.getenv('SASL_USERNAME')
sasl_password=os.getenv('SASL_PASSWORD')


c = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': f'deloton_stream' +str(uuid.uuid1()),
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
values=[]
cont=True
topic='deloton'

c.subscribe([topic])
while cont==True:
    try:
        message=c.poll(1.0)
        if message is None:
            print('None')
        else:
            print(message.value().decode())
        
    except KeyboardInterrupt:
        c.close()