# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-08-22 15:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wkplanet', '0016_miningprocess_musicprocess'),
    ]

    operations = [
        migrations.AlterField(
            model_name='realestate',
            name='work_hours',
            field=models.IntegerField(default=1000),
        ),
    ]
