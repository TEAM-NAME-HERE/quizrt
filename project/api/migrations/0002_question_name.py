# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-27 17:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='name',
            field=models.CharField(default='', max_length=255),
        ),
    ]