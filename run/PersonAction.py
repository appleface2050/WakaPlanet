# -*- coding: utf-8 -*-
import datetime
import sys
import os

from django.db import transaction

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WakaPlanet.settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

from wkplanet.models import CurrentDate, Person, InventoryFood, DoLog, PersonSkill, PersonDesire, Action, \
    PaintingProcess, MusicProcess, MiningProcess, RealEstate


class PersonAction(object):
    def __init__(self):
        self.AVAILABLE_HOUR = 16

    def cal_production_or_effort(self, act, skill_exp):
        if act == "farming":
            return round((1 * skill_exp / 1000.) / 8.0, 3)
        elif act == "do painting":
            return round((1 * skill_exp / 1000.), 3)
        elif act == "do music":
            return round((1 * skill_exp / 1000.), 3)
        elif act == "do mining":
            return round((1 * skill_exp / 1000.), 3)
        elif act == "do house":
            return round((1 * skill_exp / 1000.), 3)

    def cal_skill_exp(self, type="product", skill=""):
        if type == "product":
            return 1
        elif type == "learn_by_book":
            pass
        elif type == "learn_by_teacher":
            pass
        elif type == "self_learn":
            return 3

    def eat_dinner(self, person, date):
        """
        吃掉1个食物
        """
        try:
            with transaction.atomic():
                InventoryFood.eat_dinner(person.pk)
                DoLog.insert_a_data(person.pk, "eat_dinner", "success", date, 0)
        except Exception, e:
            print e
            print "eat dinner error ~~"
            transaction.rollback()
        else:
            transaction.commit()

    def do(self, person, act, result, act_date, act_hour):
        """
        一个小时从事的活动
        """
        print "act: ", act
        try:
            with transaction.atomic():
                if act is None:
                    raise Exception("act is none")
                if act == "farming":
                    number = self.cal_production_or_effort(act, PersonSkill.get_person_skill_exp(person_id=person.pk, skill=act))
                    InventoryFood.do_add_food_by_farming(person.pk, act, number)  # 增加产出
                    PersonSkill.add_person_skill_exp(person.pk, act, self.cal_skill_exp())  # 增加经验
                elif act == "farming upgrade":
                    PersonSkill.add_person_skill_exp(person.pk, "farming", self.cal_skill_exp(type="self_learn"))
                elif act == "painting upgrade":
                    PersonSkill.add_person_skill_exp(person.pk, "painting", self.cal_skill_exp(type="self_learn"))
                elif act == "music upgrade":
                    PersonSkill.add_person_skill_exp(person.pk, "music", self.cal_skill_exp(type="self_learn"))
                elif act == "building upgrade":
                    PersonSkill.add_person_skill_exp(person.pk, "building", self.cal_skill_exp(type="self_learn"))
                elif act == "mining upgrade":
                    PersonSkill.add_person_skill_exp(person.pk, "mining", self.cal_skill_exp(type="self_learn"))
                elif act == "do painting":
                    effort = self.cal_production_or_effort(act, PersonSkill.get_person_skill_exp(person_id=person.pk,
                                                                                                 skill="painting"))
                    PaintingProcess.add_effort(person.pk, act_date, 1, effort)
                    PersonSkill.add_person_skill_exp(person.pk, "painting", self.cal_skill_exp())
                elif act == "do music":
                    effort = self.cal_production_or_effort(act, PersonSkill.get_person_skill_exp(person_id=person.pk,
                                                                                                 skill="music"))
                    MusicProcess.add_effort(person.pk, act_date, 1, effort)
                    PersonSkill.add_person_skill_exp(person.pk, "music", self.cal_skill_exp())
                elif act == "do house":
                    effort = self.cal_production_or_effort(act, PersonSkill.get_person_skill_exp(person_id=person.pk,
                                                                                                 skill="building"))
                    RealEstate.add_effort(person.pk, effort)
                    PersonSkill.add_person_skill_exp(person.pk, "building", self.cal_skill_exp())
                elif act == "do mining":
                    effort = self.cal_production_or_effort(act, PersonSkill.get_person_skill_exp(person_id=person.pk,
                                                                                                 skill="mining"))
                    MiningProcess.mining_effort(person.pk, "ruby", effort)
                    PersonSkill.add_person_skill_exp(person.pk, "mining", self.cal_skill_exp())
                else:
                    print act
                DoLog.insert_a_data(person.pk, act, result, act_date, act_hour)
        except Exception, e:
            print e
            # print "Do error"
            transaction.rollback()
        else:
            transaction.commit()

    def act(self, person, date):
        """
        某人一天从事的活动
        """
        p_cache = {}
        print person.first_name, " ", person.last_name, date
        for hour in range(1, self.AVAILABLE_HOUR + 1):
            print "hour:", hour
            if p_cache.get("check_if_have_food_for_one_day", False) or InventoryFood.check_if_have_food_for_one_day(
                    person.pk):
                if not p_cache.get("check_if_have_food_for_one_day", False):
                    p_cache["check_if_have_food_for_one_day"] = True
                    print "有吃的"
                    # doto：处理有吃的的时候根据desire进行活动
                desires = PersonDesire.get_desire_by_person_id(person.pk)
                print "desires: ", desires
                act, desire = Action.get_person_action_by_desire(person, desires)
                # act = "farming upgrade"
            else:
                print "没吃的"
                act = "farming"

            self.do(person, act, "", date, hour)

            "先看仓库是否还有1个食物，如果没有就farm直到出了一个食物"
            "然后根据愿望开展行为"

    def all_person_one_day_action(self, date):
        print "all person one day action"
        print date
        persons = Person.get_all_alive_person()
        for p in persons:
            self.act(p, date)
            self.eat_dinner(p, date)


if __name__ == '__main__':
    now = datetime.datetime.now()
    today = CurrentDate.get_current_date()
    a = PersonAction()
    a.all_person_one_day_action(today)
    print datetime.datetime.now() - now
