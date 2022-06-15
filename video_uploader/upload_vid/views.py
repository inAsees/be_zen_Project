from django.shortcuts import render, redirect
from .forms import VideoForm


def extract_srt(request):
    if request.method == "GET":
        form = VideoForm()
        return render(request, "index.html", {"form": form})

    form = VideoForm(request.POST, request.FILES)
    if not form.is_valid():
        form = VideoForm()
        return render(request, "index.html", {"form": form})
    form.save()
    return redirect(extract_srt)
