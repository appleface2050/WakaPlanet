# coding=utf-8

# import os, sys
#
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.append(BASE_DIR)
# from django.core.wsgi import get_wsgi_application
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bst_server.settings")
# application = get_wsgi_application()
# from bst_server.settings import ENVIRONMENT

from pymongo import MongoClient
mgclient = MongoClient()
username = "root"
password = "Bluestacks2017"

# if ENVIRONMENT == "win_test":
#     mgclient = MongoClient('101.201.42.93', 3717)

CONN_ADDR1 = 'dds-2ze99c409d90d9d41.mongodb.rds.aliyuncs.com:3717'
CONN_ADDR2 = 'dds-2ze99c409d90d9d42.mongodb.rds.aliyuncs.com:3717'
REPLICAT_SET = 'mgset-3150543'
mgclient = MongoClient([CONN_ADDR1, CONN_ADDR2], replicaSet=REPLICAT_SET)

# elif ENVIRONMENT == "aliyun":
#     CONN_ADDR1 = 'dds-2ze99c409d90d9d41.mongodb.rds.aliyuncs.com:3717'
#     CONN_ADDR2 = 'dds-2ze99c409d90d9d42.mongodb.rds.aliyuncs.com:3717'
#     REPLICAT_SET = 'mgset-3150543'
#     mgclient = MongoClient([CONN_ADDR1, CONN_ADDR2], replicaSet=REPLICAT_SET)

print mgclient
mgclient.admin.authenticate(username, password)

if __name__ == '__main__':
    data = mgclient.appcenter.init_rec_like_dislike.find_one({"user_id": "abc"})
    print data