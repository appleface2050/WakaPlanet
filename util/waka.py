# coding=utf-8

import requests
import json


def name_generator():
    """
    https://uinames.com/api/?region=england
    https://uinames.com/api/?region=United%20States
    """
    count = 0
    done = False
    a = None
    while count <= 10 and not done:
        try:
            a = requests.get("https://uinames.com/api/?region=United%20States", timeout=5)
        except requests.exceptions.ConnectTimeout, e:
            print e
        if a:
            return json.loads(a.text)
        count += 1
    return None


if __name__ == '__main__':
    print name_generator()
