import os
import subprocess
from typing import List, Dict

import pysrt

from ccextractor_win.src_path import exe_file_path


class SrtExtractor:
    def __init__(self, vid_file: str, srt_file_path: str):
        self._vid_file = vid_file
        self._srt_file_path = srt_file_path
        self._subprocess_code = None

    def extract_srt_file(self) -> None:
        process = subprocess.run(
            [exe_file_path, self._vid_file, '-o', self._srt_file_path],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self._subprocess_code = process.returncode
        return None

    def is_subprocess_successful(self) -> bool:
        return self._subprocess_code == 0


class GetTimeStamps:
    def __init__(self, srt_file_path: str):
        self._srt_file_path = srt_file_path

    def get_time_stamps(self, text: str) -> List[Dict]:
        sub_list = pysrt.open(self._srt_file_path)
        time_stamps = []
        for sub in sub_list:
            if text.lower() in sub.text.lower():
                dic = {
                    "start": str(sub.start.to_time()),
                    "end": str(sub.end.to_time())
                }
                time_stamps.append(dic)
        return time_stamps


class DeleteSrtFile:
    def __init__(self, srt_file_path: str):
        self._srt_file_path = srt_file_path

    def delete_srt_file(self) -> None:
        if os.path.exists(self._srt_file_path):
            os.remove(self._srt_file_path)
        return None
