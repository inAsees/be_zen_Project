import json
import uuid
from pathlib import Path
from typing import Optional, List, Dict
import boto3
import pysrt
from boto3.dynamodb.conditions import Key
from django.http import HttpResponse
from django.template import loader

from .tasks import strip_cc_and_upload


def index(request):
    template = loader.get_template('subtitle_search/index.html')
    context = {}
    return HttpResponse(template.render(context, request))


def extract_cc(request):
    vid_file_path = str(Path(json.loads(request.body).get("filePath")))
    uid = str(uuid.uuid4())
    strip_cc_and_upload.delay(vid_file_path, uid)
    data = json.dumps({"id": uid})
    return HttpResponse(data, content_type='application/json charset=utf-8')


def get_time_stamps_for_keyword(request):
    req_json = json.loads(request.body)
    dynamo_id = req_json.get("id")
    search_text = req_json.get("text")

    dyn_resource = boto3.resource('dynamodb', region_name="ap-south-1")
    table = dyn_resource.Table('store_keywords')

    filtering_exp = Key("partition_key").eq(dynamo_id)
    str_res = table.query(KeyConditionExpression=filtering_exp).get("Items", [{}])[0].get("srt_file")

    print(str_res)
    res = GetTimeStamps(str_res, search_text).get_time_stamps()
    res_str = json.dumps({"timestamps": res})
    return HttpResponse(res_str, content_type='application/json charset=utf-8')


class GetTimeStamps:
    def __init__(self, srt_content: str, keywords: str):
        self._srt_content = srt_content
        self._keywords = keywords

    def get_time_stamps(self) -> Optional[List[Dict]]:
        sub_list = pysrt.from_string(self._srt_content)
        time_stamps = []
        for sub in sub_list:
            if self._keywords.lower() in sub.text.lower():
                dic = {
                    "start": str(sub.start.to_time()),
                    "end": str(sub.end.to_time())
                }
                time_stamps.append(dic)
        return time_stamps
