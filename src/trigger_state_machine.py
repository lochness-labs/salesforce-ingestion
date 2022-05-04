import os
import json
import boto3
import logging
from datetime import datetime

logging.getLogger().setLevel(logging.INFO)

sf_client = boto3.client('stepfunctions')
s3 = boto3.resource('s3')

STATE_MACHINE_ARN = os.getenv('STATE_MACHINE_ARN', 'ERROR_STATE_MACHINE_ARN')

def handler(event, context):

    try:
        # Bucket Name where file was uploaded
        source_bucket_name = event['Records'][0]['s3']['bucket']['name']

        # Filename of object (with path)
        file_key_name = event['Records'][0]['s3']['object']['key']

    except Exception as e:
        raise e
    
    execution_time = int(datetime.now().timestamp())

    # Start state machine execution
    response = sf_client.start_execution(
        stateMachineArn=STATE_MACHINE_ARN,
        input=json.dumps({
            'Bucket': source_bucket_name,
            'Key': file_key_name,
            'ExecutionTime': execution_time
        })
    )

    return json.dumps(response, default = datetimeConverter)

def datetimeConverter(item):
    if isinstance(item, datetime):
        return item.__str__()