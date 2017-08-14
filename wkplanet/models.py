# coding=utf-8
from __future__ import unicode_literals

from django.db import models, transaction
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
1 足够的食物（个人或家庭） （必须）
2 家庭住房生小孩
3 小孩教育
4 卓越的技能
5 伟大的作品
6 卓越的次要技能
7 伟大的次要技能作品
8 娱乐

需求权重+性格权重生成愿望列表，人根据愿望列表分配时间

愿望：
1 最多3个
2 完成一个愿望后才能增加一个新的
3 足够食物不是愿望，单独进行优先满足不占愿望名额


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


# class PropertyType(JSONBaseModel):
#     name = models.CharField(max_length=128, unique=True, null=False, blank=False)
#     uptime = models.DateTimeField(auto_now=True, verbose_name=u'数据更新时间')

class PropertyType(object):
    groups = [
        "food"
        "ruby"
    ]


class InventoryFood(JSONBaseModel):
    person_id = models.IntegerField(default=0, null=False, blank=False)
    property = models.CharField(default="", max_length=128, unique=False, null=False, blank=False)
    inventory = models.FloatField(default=0.0, null=False, blank=False)
    uptime = models.DateTimeField(auto_now=True, verbose_name=u'数据更新时间')

    @classmethod
    def eat_dinner(cls, person_id, property="farming"):
        if not cls.check_if_have_food_for_one_day(person_id):
            raise Exception("do not have enouph food!!!")
        else:
            a = cls.objects.get(person_id=person_id, property=property)
            a.inventory -= 1
            try:
                a.save()
            except Exception, e:
                print e
                print "eat dinner error"

    @classmethod
    def do_add_food_by_farming(cls, person_id, property, number):
        if cls.objects.filter(person_id=person_id, property=property).exists():
            a = cls.objects.get(person_id=person_id, property=property)
            a.inventory += number
        else:
            a = cls()
            a.person_id = person_id
            a.property = property
            a.inventory = number
        a.save()

    @classmethod
    def check_if_have_food_for_one_day(cls, person_id):
        """
        8个食物
        """
        # print "check_if_have_food_for_one_day"
        if cls.objects.filter(person_id=person_id).exists():
            foods = cls.objects.filter(person_id=person_id)
            for i in foods:
                if i.inventory >= 1.0:
                    return True
        return False


class PropertyInventory(JSONBaseModel):
    person_id = models.IntegerField(default=0, null=False, blank=False)
    property = models.CharField(default="", max_length=128, unique=False, null=False, blank=False)
    inventory = models.FloatField(default=0.0, null=False, blank=False)
    uptime = models.DateTimeField(auto_now=True, verbose_name=u'数据更新时间')


class RealEstate(JSONBaseModel):
    work_hours = models.IntegerField(default=0, null=False, blank=False)
    belong = models.IntegerField(default=0, null=False, blank=False, verbose_name=u'所属人')
    uptime = models.DateTimeField(auto_now=True, verbose_name=u'数据更新时间')


class Skill(object):
    groups = ["farming", "building", "music", "painting", "mining"]


class PersonSkill(JSONBaseModel):
    person_id = models.IntegerField(default=0, null=False, blank=False)
    skill = models.CharField(default="", max_length=128, unique=False, null=False, blank=False)
    exp = models.IntegerField(default=1000, null=False, blank=False)
    uptime = models.DateTimeField(auto_now=True, verbose_name=u'数据更新时间')

    @classmethod
    def get_person_skill_exp(cls, person_id, skill):
        exp = cache.get("get_person_skill_exp@%s@%s" % (str(person_id), skill))
        if not exp:
            if not cls.objects.filter(person_id=person_id, skill=skill).exists():
                exp = 1000
            else:
                a = cls.objects.get(person_id=person_id, skill=skill)
                exp = a.exp
            cache.set("get_person_skill_exp@%s@%s" % (str(person_id), skill), exp, 10)
        return exp

    @classmethod
    def init_person_skill_exp_if_not_exist(cls, person_id, skill):
        if cls.objects.filter(person_id=person_id, skill=skill).exists():
            return "init_person_skill_exp person skill exist"
        else:
            a = cls()
            a.person_id = person_id
            a.skill = skill
            a.save()

    @classmethod
    def add_person_skill_exp(cls, person_id, skill, exp):
        if not cls.objects.filter(person_id=person_id, skill=skill).exists():
            cls.init_person_skill_exp_if_not_exist(person_id, skill)

        a = cls.objects.get(person_id=person_id, skill=skill)
        a.exp += exp
        a.save()
        return a.exp


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
    def get_all_alive_person(cls):
        return cls.objects.filter(dead=False)

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
            with transaction.atomic():
                p.save()
                PersonCharacter.create_new_person_character(p.pk)
                print name_dict
        except Exception, e:
            print e
            print "create_a_origin_person error"


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


class Character(object):
    """
    性格
    每个人都有这6个倾向，1-9倾向程度
    """
    groups = ["追求安全感", "追求财富", "追求家庭生活", "追求艺术", "追求技术", "追求娱乐"]


class PersonCharacter(JSONBaseModel):
    person_id = models.IntegerField(default=0, null=False, blank=False)
    character = models.CharField(default="", max_length=128, unique=False, null=False, blank=False)
    value = models.IntegerField(default=5, null=False, blank=False)
    uptime = models.DateTimeField(auto_now=True, verbose_name=u'数据更新时间')

    @classmethod
    def create_new_person_character(cls, person_id):
        if not Person.objects.filter(pk=person_id).exists():
            raise Exception("person not exist")
        else:
            for c in Character.groups:
                a = cls()
                a.person_id = person_id
                a.character = c
                a.value = random.randint(1, 9)
                a.save()


class Desire(object):
    """
    愿望
    """
    # groups = ["farming", "building", "music", "painting", "mining"]
    groups = ["提升主要技能", "学习一项新的娱乐技能", "提升主要娱乐技能", "提升farming", "提升building", "提升mining", "提升music", "提升painting",
              # 技能提升
              "升级房子", "创作music", "创作painting", "mining",  # 明确使用技能进行生产
              "存储更多食物", "结婚", "生小孩"  # 愿望
              ]


class PersonDesire(JSONBaseModel):
    person_id = models.IntegerField(default=0, null=False, blank=False)
    desire = models.CharField(default="", max_length=128, unique=False, null=False, blank=False)
    uptime = models.DateTimeField(auto_now=True, verbose_name=u'数据更新时间')


class DoLog(JSONBaseModel):
    person_id = models.IntegerField(default=0, null=False, blank=False)
    act = models.CharField(default="", max_length=128, unique=False, null=False, blank=False)
    result = models.CharField(default="", max_length=128, unique=False, null=False, blank=False)
    act_date = models.DateField(null=True, verbose_name=u'行为时间', blank=True)
    act_hour = models.IntegerField(default=0, null=False, blank=False, verbose_name=u'行为小时')
    uptime = models.DateTimeField(auto_now=True, verbose_name=u'数据更新时间')

    @classmethod
    def insert_a_data(cls, person_id, act, result, act_date, act_hour):
        a = cls()
        a.person_id = person_id
        a.act = act
        a.result = result
        a.act_date = act_date
        a.act_hour = act_hour
        try:
            a.save()
        except Exception, e:
            print e

# class Demand(JSONBaseModel):
#     """
#     需求
#     """
#     pass
