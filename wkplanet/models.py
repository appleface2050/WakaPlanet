# coding=utf-8
from __future__ import unicode_literals

from django.db import models
import datetime
# Create your models here.
from util.basemodel import JSONBaseModel
from django.utils import timezone
from django.core.cache import cache


class PropertyType(JSONBaseModel):
    name = models.CharField(max_length=128, unique=True, null=False, blank=False)
    uptime = models.DateTimeField(auto_now=True, verbose_name=u'数据更新时间')


class RealEstate(JSONBaseModel):
    work_hours = models.IntegerField(default=0, null=False, blank=False)
    belong = models.IntegerField(default=0, null=False, blank=False, verbose_name=u'所属人')
    uptime = models.DateTimeField(auto_now=True, verbose_name=u'数据更新时间')


class Skill(JSONBaseModel):
    name = models.CharField(max_length=128, unique=True, null=False, blank=False)
    uptime = models.DateTimeField(auto_now=True, verbose_name=u'数据更新时间')

class SkillPerson(JSONBaseModel):
    skill_id = models.IntegerField(default=0, null=False, blank=False)
    person_id = models.IntegerField(default=0, null=False, blank=False)
    uptime = models.DateTimeField(auto_now=True, verbose_name=u'数据更新时间')

class PropertyInventory(JSONBaseModel):
    person_id = models.IntegerField(default=0, null=False, blank=False)
    property_id = models.IntegerField(default=0, null=False, blank=False)
    inventory = models.FloatField(default=0.0, null=False, blank=False)
    uptime = models.DateTimeField(auto_now=True, verbose_name=u'数据更新时间')


class Person(JSONBaseModel):
    first_name = models.CharField(max_length=256, unique=False, null=False, blank=False)
    last_name = models.CharField(max_length=256, unique=False, null=False, blank=False)
    gender = models.CharField(max_length=16, unique=False, null=False, blank=False)
    date_of_birth = models.DateTimeField(default=timezone.now, verbose_name=u'生日', blank=True)
    join_date = models.DateTimeField(default=timezone.now, verbose_name=u'进入日期', blank=True)
    parent_mother = models.IntegerField(default=0, null=False, blank=True)
    parent_father = models.IntegerField(default=0, null=False, blank=True)
    dead = models.BooleanField(default=False, null=False, verbose_name=u'是否死亡')
    date_of_dead = models.DateTimeField(null=True, verbose_name=u'死亡日期', blank=True)
    uptime = models.DateTimeField(auto_now=True, verbose_name=u'数据更新时间')

class CurrentDate(JSONBaseModel):
    current_date = models.DateTimeField(default=timezone.now, verbose_name=u'进行到的日期', blank=True)
    uptime = models.DateTimeField(auto_now=True, verbose_name=u'数据更新时间')

    @classmethod
    def get_current_date(cls):
        data = cache.get("get_current_date")
        if not data:
            if not cls.objects.all().exists():
                raise Exception("current date no data")
            else:
                data = cls.objects.all()[0].current_date
            cache.set("get_current_date", data, 3600)
        return data

    @classmethod
    def set_current_date(cls, current):
        if not cls.objects.all().exists():
            raise Exception("current date no data")
        try:
            cls.objects.update({"current_date": current})
            cache.set("get_current_date", current, 3600)
        except Exception, e:
            print e
