from pathlib import Path
from django.contrib import messages
from django.shortcuts import render, redirect
from backend_core.subtitle_extractor import SubtitleExtractor
from .forms import VideoForm


def extract_srt(request):
    if request.method == "GET":
        form = VideoForm()
        return render(request, "index.html", {"form": form})

    form = VideoForm(request.POST, request.FILES)
    if not form.is_valid():
        form = VideoForm()
        return render(request, "index.html", {"form": form})
    file_path = Path(form.cleaned_data['myfile'].temporary_file_path())
    file_name = Path(form.cleaned_data['myfile'].name).stem
    sub_extractor = SubtitleExtractor(str(file_path), file_name)
    sub_extractor.extract_srt_file()
    if not sub_extractor.is_subprocess_successful():
        messages.error(request,  "Subtitle extraction failed. Please try again or make sure video contain subtitles.")
        return redirect(extract_srt)
    messages.success(request, "Subtitle extraction successful. Please wait while we upload your video to S3 Bucket.")
    form.save()
    return redirect(extract_srt)
