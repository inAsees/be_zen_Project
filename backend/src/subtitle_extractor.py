import pysrt
import subprocess
from typing import Tuple, List
from ccextractor_win.src_path import exe_file_path
from media.src_path import video_file_path, srt_file_path


class SubtitleExtractor:
    def __init__(self):
        pass

    @staticmethod
    def extract_srt_file() -> None:
        subprocess.run([exe_file_path, video_file_path])

    @staticmethod
    def get_time_stamps(text: str) -> List[Tuple]:
        sub_list = pysrt.open(srt_file_path)
        time_stamps = []
        for sub in sub_list:
            if text.lower() in sub.text.lower():
                start = str(sub.start.to_time())
                end = str(sub.end.to_time())
                time_stamps.append((start, end))
        return time_stamps


if __name__ == '__main__':
    extractor = SubtitleExtractor()
    extractor.extract_srt_file()
    extractor.get_time_stamps("what?")
