# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-16 06:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auv', '0007_auto_20161016_0552'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auv',
            name='address',
        ),
    ]
