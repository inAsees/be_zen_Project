from django.urls import path

from . import views

urlpatterns = [
    path("", views.extract_srt, name="index"),
    path("search_subtitle/", views.search_subtitle, name="search_subtitle"),
]
