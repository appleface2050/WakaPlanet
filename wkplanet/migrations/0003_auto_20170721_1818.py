# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-07-21 18:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('wkplanet', '0002_auto_20170721_1740'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='date_of_birth',
            field=models.DateField(blank=True, default=django.utils.timezone.now, verbose_name='\u751f\u65e5'),
        ),
        migrations.AlterField(
            model_name='person',
            name='date_of_dead',
            field=models.DateField(blank=True, null=True, verbose_name='\u6b7b\u4ea1\u65e5\u671f'),
        ),
        migrations.AlterField(
            model_name='person',
            name='join_date',
            field=models.DateField(blank=True, default=django.utils.timezone.now, verbose_name='\u8fdb\u5165\u65e5\u671f'),
        ),
    ]
