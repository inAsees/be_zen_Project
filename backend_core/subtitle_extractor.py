import subprocess
from typing import Tuple, List
import pysrt
from ccextractor_win.src_path import exe_file_path
from file_path import srt_file


class SubtitleExtractor:
    def __init__(self, vid_file: str, file_name: str):
        self._vid_file = vid_file
        self._srt_file = srt_file
        self._file_name = file_name
        self._subprocess_code = None

    def extract_srt_file(self) -> None:
        process = subprocess.run(
            [exe_file_path, self._vid_file, '-o', '{}/{}.srt'.format(self._srt_file, self._file_name)],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self._subprocess_code = process.returncode
        return None

    def is_subprocess_successful(self) -> bool:
        return self._subprocess_code == 0

    def get_time_stamps(self, text: str) -> List[Tuple]:
        sub_list = pysrt.open(self._srt_file)
        time_stamps = []
        for sub in sub_list:
            if text.lower() in sub.text.lower():
                start = str(sub.start.to_time())
                end = str(sub.end.to_time())
                time_stamps.append((start, end))
        return time_stamps
