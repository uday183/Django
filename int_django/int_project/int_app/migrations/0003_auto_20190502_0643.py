# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-05-02 06:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('int_app', '0002_auto_20190502_0641'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdetails',
            name='address',
        ),
        migrations.AddField(
            model_name='userdetails',
            name='address',
            field=models.ManyToManyField(to='int_app.Address'),
        ),
    ]
