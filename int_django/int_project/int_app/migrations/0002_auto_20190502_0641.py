# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-05-02 06:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('int_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pin', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='userdetails',
            name='address',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='int_app.Address'),
            preserve_default=False,
        ),
    ]
