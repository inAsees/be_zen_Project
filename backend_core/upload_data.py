import os
import uuid

import boto3
from dotenv import load_dotenv

load_dotenv()


class UploadKeywords:
    def __init__(self, srt_file_path: str, keywords: str):
        self._srt_file_path = srt_file_path
        self._keywords = keywords

    def upload_srt_and_keyword(self, dyn_resource=None):
        if dyn_resource is None:
            dyn_resource = boto3.resource(
                'dynamodb',
                aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
            )
        table = dyn_resource.Table('store_keywords')

        with open(self._srt_file_path, 'rb') as f:
            srt_file = f.read()

        table.put_item(Item={
            'partition_key': str(uuid.uuid4()),
            'keywords': self._keywords,
            'srt_file': srt_file,
        })
