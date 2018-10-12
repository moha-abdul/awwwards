from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    profile_bio = models.CharField(max_length=50)
    profile_photo  = models.ImageField(upload_to = 'profile/')

    def __str__(self):
        return self.bio

    def save_image(self):
        self.save()

    def delete_image(self):
        self.delete()
