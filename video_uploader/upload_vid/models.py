from django.db import models


# Create your models here.

class VideoUpload(models.Model):
    myfile = models.FileField(upload_to='videos/')
