# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-03 00:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('check', '0002_ping_db_slave_hostname'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='monitor_db',
            name='id',
        ),
        migrations.AlterField(
            model_name='monitor_db',
            name='target',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
    ]
