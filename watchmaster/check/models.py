from __future__ import absolute_import, unicode_literals
from django.db import models

# Create your models here.



class ping_db(models.Model):
        target=models.CharField(max_length=50)
	slave_hostname=models.CharField(max_length=50,default="HI")
        result=models.CharField(max_length=1000)
        timestamp=models.DateTimeField(auto_now_add=True)

class monitor_db(models.Model):
        target=models.CharField(max_length=50,primary_key=True)
        test=models.CharField(max_length=50)


