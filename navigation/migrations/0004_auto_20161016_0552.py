# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-16 05:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('navigation', '0003_auto_20161016_0438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='auv',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trips', to='auv.AUV'),
        ),
    ]