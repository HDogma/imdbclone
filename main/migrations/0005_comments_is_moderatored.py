# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-01-05 09:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20170104_0932'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='is_moderatored',
            field=models.BooleanField(default='False'),
            preserve_default=False,
        ),
    ]
