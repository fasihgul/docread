from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator


def content_file_name(instance, filename):
    return '/'.join(['', instance.user.username, filename])


class Topics(models.Model):
     id = models.AutoField(primary_key=True)
     short_des =  models.CharField(max_length=255,unique=True)
     long_des = models.TextField()
     date_created = models.DateTimeField(default = timezone.now) 




class Folder(models.Model):
    path =  models.CharField(max_length=255,unique=True)
    folder_id = models.AutoField(primary_key=True)
    date_created = models.DateTimeField(default = timezone.now)
    topics = models.ManyToManyField(Topics, related_name='folders_topics')



class Documents(models.Model):
    id = models.AutoField(primary_key=True)
    doc = models.FileField(validators=[
        FileExtensionValidator(allowed_extensions=['txt','pdf'])
    ])
    date_created = models.DateTimeField(default = timezone.now) 
    topics = models.ManyToManyField(Topics, related_name='document_topics')
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='folders', related_query_name='folders')

    



