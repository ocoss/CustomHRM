# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-05 01:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0005_auto_20151204_1935'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='name_slug',
            field=models.SlugField(default='telescoping_sum', unique=True),
            preserve_default=False,
        ),
    ]
