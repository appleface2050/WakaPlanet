# -*- coding: utf-8 -*-
import datetime
import sys
import os



BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WakaPlanet.settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

from wkplanet.models import CurrentDate
from run.PersonAction import PersonAction

class Process(object):
    def waka(self):
        now = datetime.datetime.now()
        print "start next day process"
        today = CurrentDate.get_current_date()
        print today
        # Person.create_a_origin_person()

        a = PersonAction()
        a.all_person_one_day_action(today)

        CurrentDate.set_next_day()
        print datetime.datetime.now() - now


if __name__ == '__main__':
    a = Process()
    a.waka()
