from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('extractcc', views.extract_cc),
    path('search', views.get_time_stamps_for_keyword),
]