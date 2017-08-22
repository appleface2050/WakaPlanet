# coding=utf-8
from __future__ import unicode_literals

from django.db import models, transaction
import datetime
import random
# Create your models here.
from util.basemodel import JSONBaseModel
from django.utils import timezone
from django.core.cache import cache

from util.waka import name_generator, random_weight_from_dict

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


class Painting(JSONBaseModel):
    person_id = models.IntegerField(default=0, null=False, blank=False, verbose_name=u'所有人')
    author = models.IntegerField(default=0, null=False, blank=False, verbose_name=u'作者')
    create_date = models.DateField(null=True, verbose_name=u'完成时间', blank=True)
    score = models.IntegerField(default=0, null=False, blank=False, verbose_name=u'评分')  # 0 - 100
    uptime = models.DateTimeField(auto_now=True, verbose_name=u'数据更新时间')

    @classmethod
    def painting_success(cls, author, create_date, score):
        a = cls()
        a.person_id = author
        a.author = author
        a.create_date = create_date
        a.score = score
        a.save()


class PaintingProcess(JSONBaseModel):
    author = models.IntegerField(default=0, null=False, blank=False, verbose_name=u'作者')
    start_date = models.DateField(null=True, verbose_name=u'完成时间', blank=True)
    work_hour = models.IntegerField(default=0, null=False, blank=False, verbose_name=u'创作时长')
    effort = models.IntegerField(default=0, null=False, blank=False)
    uptime = models.DateTimeField(auto_now=True, verbose_name=u'数据更新时间')

    @classmethod
    def add_effort(cls, author, start_date, work_hour, effort):
        if not cls.objects.filter(author=author).exists():
            a = cls()
            a.author = author
            a.start_date = start_date
            a.work_hour = work_hour
            a.effort = effort
            a.save()
        else:
            a = cls.objects.get(author=author)
            a.work_hour += work_hour
            a.effort += effort
            a.save()
            if a.work_hour >= 100:
                cls.create_painting(a.pk, author, start_date)

    @classmethod
    def create_painting(cls, painting_process_id, author, start_date):
        if cls.objects.get(pk=painting_process_id).work_hour < 100:
            raise Exception("painting work hour < 100")
        else:
            a = cls.objects.get(pk=painting_process_id)
            # 作品评分为effort/100
            score = (a.effort) / 100
            # 出个作品概率为1/100
            if random.randint(1, 100) >= 95:
                Painting.painting_success(author, start_date, score)
            a.delete()


class MiningProcess(JSONBaseModel):
    person_id = models.IntegerField(default=0, null=False, blank=False, verbose_name=u'版权所有人')
    type = models.CharField(default="ruby", max_length=128, unique=False, null=False, blank=False)
    effort = models.IntegerField(default=0, null=False, blank=False, verbose_name=u'1000点出一个ruby')
    uptime = models.DateTimeField(auto_now=True, verbose_name=u'数据更新时间')

    # @classmethod
    # def change_inventory_and_effort(cls, person_id, type):


    @classmethod
    def mining_effort(cls, person_id, type, effort):
        if cls.objects.filter(person_id=person_id, type=type).exists():
            a = cls.objects.filter(person_id=person_id, type=type)
            a.effort += effort
            a.save()
        else:
            a = cls()
            a.person_id = person_id
            a.type = type
            a.effort = effort
            a.save()

        a = cls.objects.get(person_id=person_id, type=type)
        if a.effort >= 1000:
            try:
                with transaction.atomic():
                    PropertyInventory.change_inventory(a.person_id, a.type, 1)
                    a.effort = 0
                    a.save()
            except Exception, e:
                print e
                print "MiningProcess.mining_effort error"
                transaction.rollback()
            else:
                transaction.commit()
        return True


class Music(JSONBaseModel):
    person_id = models.IntegerField(default=0, null=False, blank=False, verbose_name=u'版权所有人')
    author = models.IntegerField(default=0, null=False, blank=False, verbose_name=u'作者')
    create_date = models.DateField(null=True, verbose_name=u'完成时间', blank=True)
    score = models.IntegerField(default=0, null=False, blank=False, verbose_name=u'评分')  # 0 - 100
    uptime = models.DateTimeField(auto_now=True, verbose_name=u'数据更新时间')

    @classmethod
    def music_success(cls, author, create_date, score):
        a = cls()
        a.person_id = author
        a.author = author
        a.create_date = create_date
        a.score = score
        a.save()


class MusicProcess(JSONBaseModel):
    author = models.IntegerField(default=0, null=False, blank=False, verbose_name=u'作者')
    start_date = models.DateField(null=True, verbose_name=u'完成时间', blank=True)
    work_hour = models.IntegerField(default=0, null=False, blank=False, verbose_name=u'创作时长')
    effort = models.IntegerField(default=0, null=False, blank=False)
    uptime = models.DateTimeField(auto_now=True, verbose_name=u'数据更新时间')

    @classmethod
    def add_effort(cls, author, start_date, work_hour, effort):
        if not cls.objects.filter(author=author).exists():
            a = cls()
            a.author = author
            a.start_date = start_date
            a.work_hour = work_hour
            a.effort = effort
            a.save()
        else:
            a = cls.objects.get(author=author)
            a.work_hour += work_hour
            a.effort += effort
            a.save()
            if a.work_hour >= 100:
                cls.create_music(a.pk, author, start_date)

    @classmethod
    def create_music(cls, music_process_id, author, start_date):
        if cls.objects.get(pk=music_process_id).work_hour < 100:
            raise Exception("painting work hour < 100")
        else:
            a = cls.objects.get(pk=music_process_id)
            # 作品评分为effort/100
            score = (a.effort) / 100
            # 出个作品概率为1/100
            if random.randint(1, 100) >= 92:
                cls.music_success(author, start_date, score)
            a.delete()


class InventoryFood(JSONBaseModel):
    person_id = models.IntegerField(default=0, null=False, blank=False)
    property = models.CharField(default="", max_length=128, unique=False, null=False, blank=False)
    inventory = models.FloatField(default=0.0, null=False, blank=False)
    uptime = models.DateTimeField(auto_now=True, verbose_name=u'数据更新时间')

    @classmethod
    def get_inventory_by_person_id_property(cls, person_id, property):
        if not cls.objects.filter(person_id=person_id, property=property).exists():
            return 0
        else:
            return cls.objects.get(person_id=person_id, property=property).inventory

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

    @classmethod
    def change_inventory(cls, person_id, property, inventory_delta):
        a = cls.objects.get(person_id=person_id, property=property)
        a.inventory += inventory_delta
        a.save()


class RealEstate(JSONBaseModel):
    work_hours = models.IntegerField(default=1000, null=False, blank=False)
    person_id = models.IntegerField(default=0, null=False, blank=False, verbose_name=u'所属人')
    in_use = models.BooleanField(default=False)  # 一个人最多只有一个房子在使用
    uptime = models.DateTimeField(auto_now=True, verbose_name=u'数据更新时间')

    @classmethod
    def get_working_realestats(cls, person_id):
        if not cls.objects.filter(person_id=person_id).exists():
            a = cls()
            a.person_id = person_id
            a.in_use = True
            a.save()
            return a.pk
        if cls.objects.filter(person_id=person_id, in_use=True).exists():
            a = cls.objects.get(person_id=person_id,in_use=True)
            return a.pk
        else:
            a = cls.objects.filter(person_id=person_id)[0]
            a.in_use = True
            a.save()
            return a.pk


    @classmethod
    def get_work_hours_by_belong(cls, person_id):
        if not cls.objects.filter(person_id=person_id):  # 没房子
            return 0
        elif cls.objects.filter(person_id=person_id, in_use=True).exists():  # 有房子且房子正在使用中
            a = cls.objects.get(person_id=person_id, in_use=True)
            return a.work_hours
        else:  # 有房子房子没有在使用
            a = cls.objects.filter(person_id=person_id).order_by("-work_hours")[0]
            return a.work_hours

    @classmethod
    def add_effort(cls, person_id, effort):
        id = cls.get_working_realestats(person_id)
        a = cls.objects.get(pk=id)
        a.work_hours += effort
        a.save()

class PersonSkill(JSONBaseModel):
    person_id = models.IntegerField(default=0, null=False, blank=False)
    skill = models.CharField(default="", max_length=128, unique=False, null=False, blank=False)
    exp = models.IntegerField(default=1000, null=False, blank=False)
    uptime = models.DateTimeField(auto_now=True, verbose_name=u'数据更新时间')

    @classmethod
    def get_main_skill(cls, person_id):
        main_skill = cache.get("get_main_skill@%s" % str(person_id))
        if not main_skill:
            if cls.objects.filter(person_id=person_id).exists():
                data = cls.objects.filter(person_id=person_id).order_by("-exp")[0]
                main_skill = data.skill
            else:
                main_skill = "farming"
            cache.set("get_main_skill@%s" % str(person_id), main_skill, 3600)
        return main_skill

    @classmethod
    def get_main_entertainment_skill(cls, person_id):
        main_etm_skill = cache.get("get_main_entertainment_skill@%s" % str(person_id))
        if not main_etm_skill:
            if cls.objects.filter(person_id=person_id, skill__in=Skill.entertainment_skill).exists():
                data = cls.objects.filter(person_id=person_id, skill__in=Skill.entertainment_skill).order_by("-exp")[0]
                main_etm_skill = data.skill
                assert main_etm_skill in Skill.entertainment_skill
            else:
                main_etm_skill = random.choice(Skill.entertainment_skill)
            cache.set("get_main_entertainment_skill@%s" % str(person_id), main_etm_skill, 3600)
        return main_etm_skill

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
        print name_dict
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
                desires = Desire.generate_desire_weight_dict_by_character(p.pk)
                PersonDesire.insert_desire_data(p.pk, desires)
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


class PersonCharacter(JSONBaseModel):
    person_id = models.IntegerField(default=0, null=False, blank=False)
    character = models.CharField(default="", max_length=128, unique=False, null=False, blank=False)
    value = models.IntegerField(default=5, null=False, blank=False)
    uptime = models.DateTimeField(auto_now=True, verbose_name=u'数据更新时间')

    @classmethod
    def get_person_character_by_person_id(cls, person_id):
        result = cache.get("get_person_character_by_person_id@%s" % str(person_id))
        if not result:
            result = []
            if not cls.objects.filter(person_id=person_id).exists():
                raise Exception("person character not exist")
            else:
                data = cls.objects.filter(person_id=person_id)
                for i in data:
                    result.append(i.toJSON())
                cache.set("get_person_character_by_person_id@%s" % str(person_id), result, 3600)
        return result

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


class PersonDesire(JSONBaseModel):
    person_id = models.IntegerField(default=0, null=False, blank=False)
    desire = models.CharField(default="", max_length=128, unique=False, null=False, blank=False)
    origin = models.FloatField(default=0.0, null=False, blank=False)
    target = models.FloatField(default=0.0, null=False, blank=False)
    uptime = models.DateTimeField(auto_now=True, verbose_name=u'数据更新时间')

    @classmethod
    def delete_desire(cls, person_id, desire):
        a = cls.objects.get(person_id=person_id, desire=desire)
        a.delete()

    @classmethod
    def get_desire_by_person_id(cls, person_id):
        result = []
        if cls.desire_empty(person_id):
            desires = Desire.generate_desire_weight_dict_by_character(person_id)
            cls.insert_desire_data(person_id, desires)
        a = cls.objects.filter(person_id=person_id)
        for i in a:
            result.append(i.toJSON())
        return result

    @classmethod
    def desire_empty(cls, person_id):
        return not cls.objects.filter(person_id=person_id).exists()

    @classmethod
    def insert_desire_data(cls, person_id, desires):
        count = cls.objects.filter(person_id=person_id).count()  # 还有的desire数量
        insert_count = 3 - count
        for i in desires[:insert_count]:
            a = cls()
            a.person_id = person_id
            a.desire = i["desire"]
            a.origin = i["origin"]
            a.target = i["target"]
            a.save()


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


########################################################################################################################################################
class Skill(object):
    groups = ["farming", "building", "music", "painting", "mining"]
    entertainment_skill = ["music", "painting"]


class Character(object):
    """
    性格
    每个人都有这6个倾向，1-9倾向程度
    """
    groups = ["safty", "wealth", "family", "art", "skill", "entertainment"]


class Desire(object):
    """
    愿望
    """
    groups = ["main skill upgrade", "main entertainment skill upgrade", "farming upgrade", "building upgrade",
              "mining upgrade", "music upgrade", "painting upgrade",
              "do house", "do music", "do painting", "do mining",
              "save food", "marriage", "have a baby"
              ]

    @classmethod
    def generate_desire_weight_dict_by_character(cls, person_id):
        """
        根据character生成desire
        """
        pc = PersonCharacter.get_person_character_by_person_id(person_id)
        # print pc

        desire = {}
        for i in Desire.groups:
            desire[i] = 5  # 默认权重为5

        for c in pc:
            if c.get("character") == "safty":
                desire["save food"] += c.get("value") * 10
                desire["main skill upgrade"] += c.get("value") * 7.5
                desire["marriage"] += c.get("value") * 5
                desire["farming upgrade"] += c.get("value") * 5

            elif c.get("character") == "wealth":
                desire["save food"] += c.get("value") * 5
                desire["do mining"] += c.get("value") * 3.5
                desire["main skill upgrade"] += c.get("value") * 7.5
                desire["do house"] += c.get("value") * 7

            elif c.get("character") == "family":
                desire["do house"] += c.get("value") * 7
                desire["marriage"] += c.get("value") * 10
                desire["have a baby"] += c.get("value") * 10
                desire["building upgrade"] += c.get("value") * 5

            elif c.get("character") == "art":
                desire["do music"] += c.get("value") * 10
                desire["do painting"] += c.get("value") * 10
                desire["main entertainment skill upgrade"] += c.get("value") * 7
                desire["music upgrade"] += c.get("value") * 7
                desire["painting upgrade"] += c.get("value") * 7

            elif c.get("character") == "skill":
                desire["main skill upgrade"] += c.get("value") * 10
                desire["main entertainment skill upgrade"] += c.get("value") * 5
                desire["farming upgrade"] += c.get("value") * 1
                desire["building upgrade"] += c.get("value") * 1
                desire["mining upgrade"] += c.get("value") * 1
                desire["music upgrade"] += c.get("value") * 1
                desire["painting upgrade"] += c.get("value") * 1

            elif c.get("character") == 'entertainment':
                desire["main entertainment skill upgrade"] += c.get("value") * 5
                desire["mining upgrade"] += c.get("value") * 2
                desire["music upgrade"] += c.get("value") * 2
                desire["painting upgrade"] += c.get("value") * 2
                desire["do music"] += c.get("value") * 7
                desire["do painting"] += c.get("value") * 7

        print desire
        result = []

        for i in range(5):
            result.append(random_weight_from_dict(desire))
        result = list(set(result))[:3]
        randed_desire_list = []
        for i in result:
            # tmp = {i:desire.get(i)}
            origin, target = cls.cal_desire_origin_target(person_id, i)
            tmp = {"desire": i, "weight": desire.get(i), "person_id": person_id, "origin": origin, "target": target}
            randed_desire_list.append(tmp)
        print randed_desire_list
        return randed_desire_list

    @classmethod
    def cal_desire_origin_target(self, person_id, desire):
        origin, target = None, None
        assert desire in Desire.groups

        if desire == "main skill upgrade":
            origin, target = 0, 0
        elif desire == "main entertainment skill upgrade":
            origin, target = 0, 0
        elif desire == "farming upgrade":
            origin = PersonSkill.get_person_skill_exp(person_id, "farming")
            target = origin + 1000
        elif desire == "building upgrade":
            origin = PersonSkill.get_person_skill_exp(person_id, "building")
            target = origin + 1000
        elif desire == "mining upgrade":
            origin = PersonSkill.get_person_skill_exp(person_id, "mining")
            target = origin + 1000
        elif desire == "music upgrade":
            origin = PersonSkill.get_person_skill_exp(person_id, "music")
            target = origin + 1000
        elif desire == "painting upgrade":
            origin = PersonSkill.get_person_skill_exp(person_id, "painting")
            target = origin + 1000
        elif desire == "do house":
            origin = RealEstate.get_work_hours_by_belong(person_id)
            target = origin + 1000
        elif desire == "do music":
            origin = 0
            target = 100
        elif desire == "do painting":
            origin = 0
            target = 100
        elif desire == "do mining":
            origin = 0
            target = 1000
        elif desire == "save food":
            origin = InventoryFood.get_inventory_by_person_id_property(person_id, "farming")
            target = origin + 1000
        elif desire == "marriage":
            origin = 0
            target = 500
        elif desire == "have a baby":
            origin = 0
            target = 500
        if origin == None or target == None:
            raise Exception("origin or target is None")
        else:
            return origin, target


class Action(object):
    @classmethod
    def get_person_action_by_desire(cls, person, desires):
        assert isinstance(person, Person)
        # for desire in desires:
        desire = desires[0]
        act = desire.get("desire")
        if act == "main skill upgrade":
            main_skill = PersonSkill.get_main_skill(person.pk)
            return main_skill + " upgrade", desire
        elif act == "main entertainment skill upgrade":
            main_etm_skill = PersonSkill.get_main_entertainment_skill(person.pk)
            return main_etm_skill + " upgrade", desire
        elif act in (
                "farming upgrade", "building upgrade", "mining upgrade", "music upgrade", "painting upgrade"):
            return act, desire
        elif act in ("do house", "do music", "do painting", "do mining"):
            return act, desire
        elif act == "save food":
            return act, desire

        # todo:
        elif act == "marriage":
            return "do house", desire
        elif act == "have a baby":
            return "do house", desire
        else:
            raise Exception("desire is not good")
            print act, desire
