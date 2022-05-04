import json
import boto3
import logging
import os
import urllib.parse
from datetime import datetime
import awswrangler as wr
import pandas as pd

s3_client = boto3.client("s3")
athena_client = boto3.client("athena")

logging.getLogger().setLevel(logging.INFO)

SRC_BUCKET_PREFIX = os.getenv('SRC_BUCKET_PREFIX', 'ERROR_SRC_BUCKET_PREFIX')
DEST_BUCKET = os.getenv('DEST_BUCKET_NAME', 'ERROR_DEST_BUCKET_NAME')
DEST_KEY = os.getenv('DEST_BUCKET_PREFIX', 'ERROR_DEST_BUCKET_PREFIX')
ATHENA_RAW_DB = os.getenv('ATHENA_RAW_DB', 'ERROR_ATHENA_RAW_DB')
ATHENA_OUTPUT_BUCKET_NAME = os.getenv('ATHENA_OUTPUT_BUCKET_NAME', 'ERROR_ATHENA_OUTPUT_BUCKET_NAME')


def handler(event, context):

    # event contains all information about uploaded object
    print("Event :", event)

    event_key = urllib.parse.unquote(event['Key'])

    # Create the new key on the Data Lake
    table = event_key.replace(SRC_BUCKET_PREFIX, '').strip('/').split('/')[0] # i.e. intake/transition/saleseforce/<table_name>

    # Paths
    dest_path = f"s3://{DEST_BUCKET}/{DEST_KEY}/{table}/"
    src_path = f"s3://{event['Bucket']}/{event_key}"

    df = wr.s3.read_parquet(path=src_path)

    # Maybe apply some cleaning
    df['dumpdate'] = event['ExecutionTime']

    table = 't_salesforce_' + table.lower() + '_v1'

    # Create data and add partition to the Athena table
    ret = wr.s3.to_parquet(
        df=df,
        path=dest_path,
        dataset=True, # store a parquet dataset instead of a ordinary file
        database=ATHENA_RAW_DB,
        table=table,
        partition_cols=["dumpdate"]
    )

    print(ret)

    return {
        'statusCode': 200,
        'body': json.dumps('OK')
    }