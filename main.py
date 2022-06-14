from backend.src.subtitle_extractor import SubtitleExtractor


if __name__ == '__main__':
    extractor = SubtitleExtractor()
    extractor.extract_srt_file()
    print(extractor.get_time_stamps("what?"))