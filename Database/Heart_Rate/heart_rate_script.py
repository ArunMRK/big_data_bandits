import datetime
import boto3
from typing import NoReturn


def get_user_details(
    age: int, first: str, second: str, user_heart_rate: int,
    max_heart_rate: int, date: datetime.datetime
) -> dict:
    """Extracts al necessary user details that will need to be included in the email that will be sent - stores them in a dict
    """
    user_details = {
        "age": age, "first": first, "second": second,
        "user_heart_rate": user_heart_rate, "max_heart_rate": max_heart_rate,
        "date": str(date)
    }

    return user_details


def email_alert(user_alert_data: dict) -> NoReturn:
    """Function that sends an email to a user"""
    client = boto3.client('ses')
    response = client.send_email(
        Destination={
            'ToAddresses': [
                'big.data.bandits@gmail.com'
            ],
        },
        Message={
            'Body': {
                'Html': {
                    'Charset': 'UTF-8',
                    'Data': f"""<p>To whom it may concern, <br>
                    <br>
On <b>{user_alert_data["date"]}</b>, a user named <b>{user_alert_data["first"]} {user_alert_data["second"]}</b> aged <b>{user_alert_data["age"]}</b>, exceeded their maximum working heart rate (<b>{user_alert_data["max_heart_rate"]} bpm</b>) with a reading of <b>{user_alert_data["user_heart_rate"]} bpm</b>. <br>
<br>
Please be advised that this is not a healthy heart rate and can cause serious issues if this heart rate persists. <br>
<br>
Regards, <br>
Big Data Bandits</p>""",
                },
                'Text': {
                    'Charset': 'UTF-8',
                    'Data': 'This is for those who cannot read HTML.',
                },
            },
            'Subject': {
                'Charset': 'UTF-8',
                'Data': 'High Heart Rate Alert',
            },
        },
        Source='big.data.bandits@gmail.com',
    )
