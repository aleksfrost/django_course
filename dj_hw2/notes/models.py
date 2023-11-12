from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Note(models.Model):

    content = models.CharField(max_length=160)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
