# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-08-11 16:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wkplanet', '0004_auto_20170721_1843'),
    ]

    operations = [
        migrations.CreateModel(
            name='Demand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='PropertyType',
        ),
        migrations.DeleteModel(
            name='Skill',
        ),
        migrations.RemoveField(
            model_name='propertyinventory',
            name='property_id',
        ),
        migrations.RemoveField(
            model_name='skillperson',
            name='skill_id',
        ),
        migrations.AddField(
            model_name='propertyinventory',
            name='property',
            field=models.CharField(default='', max_length=128),
        ),
        migrations.AddField(
            model_name='skillperson',
            name='exp',
            field=models.IntegerField(default=1000),
        ),
        migrations.AddField(
            model_name='skillperson',
            name='skill',
            field=models.CharField(default='', max_length=128),
        ),
    ]
