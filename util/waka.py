# coding=utf-8

import requests
import json
import random


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
            a = requests.get("https://uinames.com/api/?region=United%20States", timeout=10)
        except requests.exceptions.ConnectTimeout, e:
            print e
        if a:
            return json.loads(a.text)
        count += 1
    return None


def windex(lst):
    '''an attempt to make a random.choose() function that makes weighted choices
    accepts a list of tuples with the item and probability as a pair'''
    wtotal = sum([x[1] for x in lst])
    n = random.uniform(0, wtotal)
    for item, weight in lst:
        if n < weight:
            break
        n = n - weight
    return item


def random_weight_from_dict(lst):
    '''an attempt to make a random.choose() function that makes weighted choices
    accepts a list of tuples with the item and probability as a pair'''
    wtotal = sum(lst.values())
    n = random.uniform(0, wtotal)
    for key in lst:
        if n < lst.get(key):
            break
        n = n - lst.get(key)
    return key


if __name__ == '__main__':
    # a = [("A",10),("B",5)]
    a = {"a": 10, "b":5}
    print random_weight_from_dict(a)
