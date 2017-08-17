# -*- coding: utf-8 -*-
import datetime
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WakaPlanet.settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

from wkplanet.models import CurrentDate, Person


if __name__ == '__main__':
    Person.create_a_origin_person()
