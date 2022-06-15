from django.shortcuts import render


def extract_srt(request):
    if request.method == "GET":
        return render(request, 'index.html')

    video_file = request.FILES["video_file"]
