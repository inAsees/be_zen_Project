from django.urls import path

from . import views

urlpatterns = [
    path("", views.extract_srt, name="index")
]
