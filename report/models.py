
from django.db import models

from registration.models import CustomUser
from videoupload.models import Video

class Report(models.Model):
    id= models.AutoField(primary_key=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Add this field
    reason = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    status=models.BooleanField(default=True)