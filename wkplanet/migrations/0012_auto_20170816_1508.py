# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-08-16 15:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wkplanet', '0011_dolog_act_hour'),
    ]

    operations = [
        migrations.AddField(
            model_name='persondesire',
            name='origin',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='persondesire',
            name='target',
            field=models.FloatField(default=0.0),
        ),
    ]
