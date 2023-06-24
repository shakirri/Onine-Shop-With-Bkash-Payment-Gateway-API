from django.db import models

# Create your models here.
class Users(models.Model):
    name = models.CharField(max_length=20, primary_key=True, serialize=False)
    agreementID = models.CharField(default=None, blank=True, null=True, max_length=50)
    phone=models.CharField(default=None, blank=True, null=True, max_length=11)
    