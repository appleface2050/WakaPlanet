# -*- coding: utf-8 -*-
import datetime
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WakaPlanet.settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

from wkplanet.model2 import Desire

if __name__ == '__main__':
    print Desire.generate_desire_weight_dict_by_character(1)
