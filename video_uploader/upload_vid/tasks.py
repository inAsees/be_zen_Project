import subprocess
import tempfile
from pathlib import Path

import boto3
from celery import shared_task


class SrtExtractor:
    def __init__(self):
        self._subprocess_code = None

    def extract_srt_file(self, vid_file: str, srt_file_path: str) -> None:
        process = subprocess.run(
            ["ccextractor", vid_file, '-o', srt_file_path],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        self._subprocess_code = process.returncode
        return None

    def is_subprocess_successful(self) -> bool:
        return self._subprocess_code == 0


class UploadData:
    @staticmethod
    def upload_video(video_file_path: str, file_name: str):
        client = boto3.resource('s3')
        bucket = client.Bucket('videos-for-extracting-srt-files')
        bucket.upload_file(Filename=video_file_path, Key=file_name)

    @staticmethod
    def upload_srt(srt_file_path: str, uid, dyn_resource=None):
        if dyn_resource is None:
            dyn_resource = boto3.resource('dynamodb', region_name="ap-south-1")
        table = dyn_resource.Table('store_keywords')

        with open(srt_file_path, 'r') as f:
            srt_file = f.read()
            table.put_item(Item={
                'partition_key': uid,
                'srt_file': srt_file,
            })


@shared_task
def strip_cc_and_upload(file_path, uid):
    temp_file_path = tempfile.NamedTemporaryFile()
    print("Temp File Path: ", "{}.srt".format(temp_file_path.name))
    SrtExtractor().extract_srt_file(file_path, "{}.srt".format(temp_file_path.name))

    UploadData.upload_video(file_path, Path(file_path).name)
    UploadData.upload_srt("{}.srt".format(temp_file_path.name), uid)
    print("SRT uploaded")
