from django import forms

from .models import VideoUpload


# Create the form class.
class VideoForm(forms.ModelForm):
    myfile = forms.FileField(label='Select a file', widget=forms.FileInput(attrs={'accept': 'video/*'}))

    class Meta:
        model = VideoUpload
        fields = ['myfile']
