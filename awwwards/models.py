from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    profile_bio = models.CharField(max_length=50)
    profile_photo  = models.ImageField(upload_to = 'profile/')

    def __str__(self):
        return self.bio

    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()

class Project(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='user')
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    projects = models.CharField(max_length=50)

    def save_project(self):
        self.save()

    def delete_project(self):
        self.delete()

# class Rating(models.Model):
#     design = models.CharField(max_length=50)
#     usability = models.CharField(max_length=50)
#     content = models.CharField(max_length=50)