from boto3 import session
from botocore.client import Config

import os
ACCESS_ID = 'EXCD2WPSZ2TWSRW6G76R'
SECRET_KEY = '6WAtkhVdMN93XRmw+HQ8wAqwbQNr879PjhYOT6hMgzw'

# Initiate session
session = session.Session()
client = session.client('s3',
                        region_name='ams3',
                        endpoint_url='https://ams3.digitaloceanspaces.com',
                        aws_access_key_id=ACCESS_ID,
                        aws_secret_access_key=SECRET_KEY,
                        )

response = client.list_buckets()
print(response)