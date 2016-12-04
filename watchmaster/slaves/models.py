from __future__ import unicode_literals

from django.db import models

# Create your models here.

class slave(models.Model):
	slave_ip=models.CharField(max_length=50,primary_key=True)
	slave_hostname=models.CharField(max_length=200)
	slave_location=models.CharField(max_length=200)
