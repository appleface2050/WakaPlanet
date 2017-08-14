# -*- coding: utf-8 -*-
import datetime
import sys
import os

from util.waka import random_weight_from_dict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WakaPlanet.settings")

from django.core.wsgi import get_wsgi_application


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
    # groups = ["提升主要技能", "提升主要娱乐技能", "提升farming", "提升building", "提升mining", "提升music", "提升painting",
    #           # 技能提升
    #           "升级房子", "创作music", "创作painting", "mining",  # 明确使用技能进行生产
    #           "存储更多食物", "结婚", "生小孩"  # 愿望
    #           ]

    groups = ["main skill upgrade", "main entertainment skill upgrade", "farming upgrade", "building upgrade",
              "mining upgrade", "music upgrade", "painting upgrade",
              "do house", "do music", "do painting", "do mining",
              "save food", "marriage", "have a baby"
              ]

    @classmethod
    def generate_desire_weight_dict_by_character(cls, person_id):
        from wkplanet.models import PersonCharacter
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
        return result


class Action(object):
    @classmethod
    def get_person_action_by_desire(cls, person, desires):
        from wkplanet.models import PersonSkill
        from wkplanet.models import Person
        assert isinstance(person, Person)
        # for desire in desires:
        desire = desires[0]
        if desire == "main skill upgrade":
            main_skill = PersonSkill.get_main_skill(person.pk)
            return main_skill + " upgrade"
        elif desire == "main entertainment skill upgrade":
            main_etm_skill = PersonSkill.get_main_entertainment_skill(person.pk)
            return main_etm_skill + " upgrade"
        elif desire in ("farming upgrade", "building upgrade", "mining upgrade", "music upgrade", "painting upgrade"):
            return desire
        elif desire in ("do house", "do music", "do painting", "do mining"):
            return desire
        elif desire == "save food":
            pass
        elif desire == "marriage":
            pass
        elif desire == "have a baby":
            pass
        else:
            raise Exception("desire is not good")
