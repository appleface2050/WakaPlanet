# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-08-14 11:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wkplanet', '0009_inventoryfood'),
    ]

    operations = [
        migrations.CreateModel(
            name='DoLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person_id', models.IntegerField(default=0)),
                ('act', models.CharField(default='', max_length=128)),
                ('result', models.CharField(default='', max_length=128)),
                ('act_date', models.DateField(blank=True, null=True, verbose_name='\u884c\u4e3a\u65f6\u95f4')),
                ('uptime', models.DateTimeField(auto_now=True, verbose_name='\u6570\u636e\u66f4\u65b0\u65f6\u95f4')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
