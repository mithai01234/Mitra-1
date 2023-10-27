
from django.db import models

from registration.models import CustomUser


class Video(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='videos/')
    # uploaded_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
    share_count = models.PositiveIntegerField(default=0)
    video_blob_name = models.CharField(max_length=255,null=True)
    thumbnail = models.ImageField(upload_to='videos/', null=True, blank=True)
    # file_url = models.URLField(blank=True, null=True)
    # thumbnail_url = models.URLField(blank=True, null=True)
    def __str__(self):
        return f"{self.id}"

class Point(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    points = models.PositiveIntegerField(default=0)
    is_share = models.IntegerField(default=0)
class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    is_like = models.BooleanField()  # True for like, False for unlike

    def __str__(self):
        return f"{self.user.name} liked {self.video.id}"

class Comment(models.Model):
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.id} is {self.text}"

