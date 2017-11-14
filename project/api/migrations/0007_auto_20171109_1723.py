# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-09 17:23
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20171102_1650'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='uuid',
            field=models.SlugField(default=uuid.uuid4, editable=False),
        ),
        migrations.AddField(
            model_name='classprofile',
            name='uuid',
            field=models.SlugField(default=uuid.uuid4, editable=False),
        ),
        migrations.AddField(
            model_name='question',
            name='uuid',
            field=models.SlugField(default=uuid.uuid4, editable=False),
        ),
        migrations.AddField(
            model_name='quiz',
            name='uuid',
            field=models.SlugField(default=uuid.uuid4, editable=False),
        ),
        migrations.AddField(
            model_name='user',
            name='uuid',
            field=models.SlugField(default=uuid.uuid4, editable=False),
        ),
    ]