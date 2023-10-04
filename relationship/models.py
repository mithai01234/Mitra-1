# models.py

from django.db import models
from registration.models import CustomUser

class Follow(models.Model):
    follower = models.ForeignKey(CustomUser, related_name='following', on_delete=models.CASCADE)
    followed = models.ForeignKey(CustomUser, related_name='followers', on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    hidden = models.BooleanField(default=False)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.follower.name} follows {self.followed.name}'
