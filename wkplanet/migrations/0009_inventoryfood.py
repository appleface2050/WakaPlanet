# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-08-11 16:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wkplanet', '0008_auto_20170811_1624'),
    ]

    operations = [
        migrations.CreateModel(
            name='InventoryFood',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person_id', models.IntegerField(default=0)),
                ('property', models.CharField(default='', max_length=128)),
                ('inventory', models.FloatField(default=0.0)),
                ('uptime', models.DateTimeField(auto_now=True, verbose_name='\u6570\u636e\u66f4\u65b0\u65f6\u95f4')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
