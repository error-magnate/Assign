from django.db import models
from django.contrib.auth.models import User


class Verify(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uid = models.CharField(max_length=5)
    pid = models.CharField(max_length=20)