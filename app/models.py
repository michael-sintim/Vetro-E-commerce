from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


# Create your models here.
class LikedItem(models.Model):
    likes = models.CharField(max_length=255)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    object_id = models.UUIDField()
    content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE)
    content_object = GenericForeignKey('content_type','object_id','')