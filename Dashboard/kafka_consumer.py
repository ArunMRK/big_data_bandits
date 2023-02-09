from confluent_kafka import Consumer
import os
import uuid

def get_kafka_messages(consumer: Consumer) -> str:
    """Gets the latest log from a Kafka consumer"""
    messages = []
    receiving_messages = True

    while receiving_messages:

        message = consumer.poll(0)
        if message is None:
            break
        messages.append(message.value().decode())
    
    consumer.commit()
    return messages
