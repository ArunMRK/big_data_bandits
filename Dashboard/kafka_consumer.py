from confluent_kafka import Consumer, KafkaError, TopicPartition, KafkaException, Producer
from dotenv import load_dotenv
import os
import uuid

load_dotenv(override=True, verbose=True)


def kafka_consumer() -> Consumer:
    """Makes a connection to a Kafka consumer"""
    c = Consumer({
        "bootstrap.servers": os.getenv("BOOTSTRAP_SERVERS"),
        "group.id": f"deloton_stream" + str(uuid.uuid1()),
        "security.protocol": "SASL_SSL",
        "sasl.mechanisms": "PLAIN",
        "sasl.username": os.getenv("SASL_USERNAME"),
        "sasl.password": os.getenv("SASL_PASSWORD"),
        "fetch.wait.max.ms": 6000,
        "auto.offset.reset": "latest",
        "enable.auto.commit": "false",
        "max.poll.interval.ms": "86400000",
        "topic.metadata.refresh.interval.ms": "-1",
        "client.id": "id-002-005",
    })
    c.subscribe(["deloton"])

    return c


def get_kafka_messages(consumer: Consumer) -> str:
    """Gets the latest log from a Kafka consumer"""
    count = 0
    messages = []
    while count < 2:
        try:
            messages.append(consumer.poll(1.0).value().decode())
            count += 1
        except:
            pass

    return messages