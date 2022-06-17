from django import forms

from .models import VideoUpload


# Create the form class.
class VideoForm(forms.ModelForm):
    myfile = forms.FileField(label='Select a file', widget=forms.FileInput(attrs={'accept': 'video/*'}), max_length=100,
                             required=True)

    class Meta:
        model = VideoUpload
        fields = ['myfile']


class SubtitleForm(forms.Form):
    text = forms.CharField(label='Enter text', max_length=200, required=True)
