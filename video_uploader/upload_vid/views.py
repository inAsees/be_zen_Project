import uuid
from pathlib import Path
from urllib.parse import urlencode
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from backend_core.handle_video_file import SrtExtractor, GetTimeStamps, DeleteSrtFile
from file_path import dir_name
from .forms import VideoForm, SubtitleForm


def extract_srt(request):
    if request.method == "GET":
        form = VideoForm()
        return render(request, "index.html", {"form": form})

    vid_form = VideoForm(request.POST, request.FILES)
    if not vid_form.is_valid():
        form = VideoForm()
        return render(request, "index.html", {"form": form})
    vid_file_path = str(Path(vid_form.cleaned_data['myfile'].temporary_file_path()))
    srt_file_path = "{}\{}.srt".format(dir_name, str(uuid.uuid4()))
    srt_extractor = SrtExtractor(vid_file_path, srt_file_path)
    srt_extractor.extract_srt_file()
    if not srt_extractor.is_subprocess_successful():
        messages.error(request, "Subtitle extraction failed. Please try again or make sure video contain subtitles.")
        DeleteSrtFile(srt_file_path).delete_srt_file()
        form = VideoForm()
        return render(request, "index.html", {"form": form})
    messages.success(request, "Subtitle extraction successful and video uploaded to S3 bucket.")
    vid_form.save()
    base_url = reverse('search_subtitle')
    query_string = urlencode({'srt_file_path': srt_file_path})
    url = '{}?{}'.format(base_url, query_string)
    return redirect(url)


def search_subtitle(request):
    if request.method == "GET":
        sub_form = SubtitleForm()
        return render(request, "subtitle_search.html", {"sub_form": sub_form})

    sub_form = SubtitleForm(request.POST)
    if not sub_form.is_valid():
        sub_form = SubtitleForm()
        return render(request, "subtitle_search.html", {"sub_form": sub_form})
    keywords = sub_form.cleaned_data['text']
    srt_file_path = request.GET.get('srt_file_path')
    time_stamps = GetTimeStamps(srt_file_path, keywords).get_time_stamps()
    if time_stamps is None:
        messages.error(request, "SRT file not found.Please try uploading the video again.")
        return redirect(extract_srt)
    elif len(time_stamps) == 0:
        messages.error(request, "No time stamps found for the given text.")
        sub_form = SubtitleForm()
        return render(request, "subtitle_search.html", {"sub_form": sub_form})

    DeleteSrtFile(srt_file_path).delete_srt_file()

    messages.success(request, "Time stamps found for the given text.")
    return render(request, "subtitle_search.html", {"time_stamps": time_stamps})
