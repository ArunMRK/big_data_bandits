import time
import json
from typing import NoReturn
import boto3

bucket_name = 'emergency-bucket-bandits'

def upload_dict_to_s3_bucket(s3: boto3.client ,heart_rate_data: dict) -> NoReturn:
    """Used for kickstarting the email SNS system to notify the user that their heart rate is exceeding the recommended limit"""

    data_to_upload = json.dumps(heart_rate_data, indent=2, default=str)
    time_now = int(time.time())
    file_name = f"{heart_rate_data['name']}{time_now}.json"
    s3.put_object(
        Bucket=bucket_name,
        Key=f'/emergencies/{file_name}',
        Body=data_to_upload
    )
