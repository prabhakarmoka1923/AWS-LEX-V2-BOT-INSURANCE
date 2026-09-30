"""Module to get the secret"""

import json
import os
import boto3
from botocore.exceptions import ClientError


def get_secret():
    """Get secret key value from secret manager"""
    secret_name = os.environ['SMARN']
    client = boto3.client('secretsmanager')

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as client_error:
        raise client_error

    secret = get_secret_value_response['SecretString']
    return json.loads(secret)
