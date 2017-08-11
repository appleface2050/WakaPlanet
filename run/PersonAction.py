# -*- coding: utf-8 -*-
import datetime
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WakaPlanet.settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

from wkplanet.models import CurrentDate, Person, Desire


class PersonAction(object):
    def __init__(self):
        self.AVAILABLE_HOUR = 16

    def act(self, person, date):
        for hour in range(1, self.AVAILABLE_HOUR+1):
            print hour
            "先看仓库是否还有1个食物，如果没有就farm直到出了一个食物"
            "然后根据愿望开展行为"



        print person.first_name, " ", person.last_name, date

    def all_person_one_day_action(self, date):
        print "all person one day action"
        print date
        persons = Person.get_all_alive_person()
        for p in persons:
            self.act(p, date)


if __name__ == '__main__':
    now = datetime.datetime.now()
    today = CurrentDate.get_current_date()
    a = PersonAction()
    a.all_person_one_day_action(today)
    print datetime.datetime.now() - now
