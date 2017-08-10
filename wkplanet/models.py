# coding=utf-8
from __future__ import unicode_literals

from django.db import models
import datetime
import random
# Create your models here.
from util.basemodel import JSONBaseModel
from django.utils import timezone
from django.core.cache import cache

from util.waka import name_generator

"""
#todo:
    2 小孩成年赠送物品
    3 遗产分配
"""

"""
规则:
时间分配决策：
0 不同人的时间分配受当前人生状况和性格影响
1 每人每天可利用时间为16小时
2 使用同一种技能进行的生产活动最多每天8小时
3 学习同一种技能技能每天最多6小时

需求：
1 足够的食物（个人或家庭）
2 家庭住房生小孩
3 小孩教育
4 卓越的技能
5 伟大的作品
6 卓越的次要技能
7 伟大的次要技能作品


生产：
1 从事每一项生产的前提是这个生产需要的技能和场所，farm不需要场所，且默认1级farm技能
2 技能生产效率为 经验/1000 代表每小时产出的单位的数量

生产类型：
1 farm
2 building


食物：
1 来自farm
2 每人每天消耗1食物

房子：
1 没有房子的人睡大街
2 房子最少3级，可以住3人
3 房子可以升级，可以买卖


技能：
1 技能学习速度：
a 使用技能从事生产，每小时1经验
b 自我训练，每小时3经验
c 书籍训练，每小时5经验
d 教师训练，每小时6经验
2 1000经验值1级





结婚：
1 有了房子才可以结婚，有了3级房子才可以生孩子
"""


class PropertyType(JSONBaseModel):
    name = models.CharField(max_length=128, unique=True, null=False, blank=False)
    uptime = models.DateTimeField(auto_now=True, verbose_name=u'数据更新时间')


class PropertyInventory(JSONBaseModel):
    person_id = models.IntegerField(default=0, null=False, blank=False)
    property_id = models.IntegerField(default=0, null=False, blank=False)
    inventory = models.FloatField(default=0.0, null=False, blank=False)
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


class Person(JSONBaseModel):
    """
    人物
    """
    first_name = models.CharField(max_length=256, unique=False, null=False, blank=False)
    last_name = models.CharField(max_length=256, unique=False, null=False, blank=False)
    gender = models.CharField(choices=[("male", "male"), ("female", "female")], max_length=16, unique=False, null=False,
                              blank=False)
    date_of_birth = models.DateField(default=timezone.now, verbose_name=u'生日', blank=True)
    join_date = models.DateField(default=timezone.now, verbose_name=u'进入日期', blank=True)
    parent_mother = models.IntegerField(default=0, null=False, blank=True)
    parent_father = models.IntegerField(default=0, null=False, blank=True)
    dead = models.BooleanField(default=False, null=False, verbose_name=u'是否死亡')
    date_of_dead = models.DateField(null=True, verbose_name=u'死亡日期', blank=True)
    uptime = models.DateTimeField(auto_now=True, verbose_name=u'数据更新时间')

    @classmethod
    def create_a_origin_person(cls):
        p = cls()
        name_dict = name_generator()
        p.first_name = name_dict.get("name")
        p.last_name = name_dict.get("surname")
        p.gender = name_dict.get("gender")
        p.date_of_birth = CurrentDate.get_current_date() - datetime.timedelta(
            days=random.randint(365 * 18, 365 * 28))  # 初始年龄 18-28 之间
        p.join_date = CurrentDate.get_current_date()
        try:
            p.save()
            print name_dict
        except Exception, e:
            print e


class CurrentDate(JSONBaseModel):
    current_date = models.DateField(default=timezone.now, verbose_name=u'进行到的日期', blank=True)
    uptime = models.DateTimeField(auto_now=True, verbose_name=u'数据更新时间')

    @classmethod
    def set_next_day(cls):
        today = cls.objects.all().order_by("-uptime")[0]
        today.current_date += datetime.timedelta(days=1)
        try:
            today.save()
            cache.set("get_current_date", today.current_date, 3600)
        except Exception, e:
            print e
            print today

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
