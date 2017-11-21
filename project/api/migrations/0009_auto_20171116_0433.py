# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-16 04:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20171116_0325'),
    ]

    operations = [
        migrations.AddField(
            model_name='classprofile',
            name='name',
            field=models.CharField(default='A Profile', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quiz',
            name='name',
            field=models.CharField(default='A Quiz', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='classprofile',
            name='description',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='question',
            name='prompt',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='description',
            field=models.CharField(max_length=255),
        ),
    ]
