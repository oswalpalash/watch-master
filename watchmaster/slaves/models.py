from __future__ import unicode_literals

from django.db import models

# Create your models here.

class subordinate(models.Model):
	subordinate_ip=models.CharField(max_length=50,primary_key=True)
	subordinate_hostname=models.CharField(max_length=200)
	subordinate_location=models.CharField(max_length=200)
