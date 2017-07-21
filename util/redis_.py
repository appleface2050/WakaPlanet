# coding=utf-8

import os
import sys
import redis
import json

#这里替换为连接的实例host和port

sys.path.append(os.path.dirname(os.path.split(os.path.realpath(__file__))[0]))

from bst_android_market.settings import ENVIRONMENT, redis_client, redis_client_production

# host_production = '5c1cd0b3b9d84412.redis.rds.aliyuncs.com'
# port_production = 6379
# user_production = '5c1cd0b3b9d84412'
# pwd_production = 'Bluestackscn2016'
#
#
# if ENVIRONMENT == "aliyun":
#     redis_host = '5c1cd0b3b9d84412.redis.rds.aliyuncs.com'
#     redis_port = 6379
#     redis_user = '5c1cd0b3b9d84412'
#     reids_pwd = 'Bluestackscn2016'
# elif ENVIRONMENT == "aliyun_test_preview":
#     redis_host = 'r-2zecc8e7087281d4.redis.rds.aliyuncs.com'
#     redis_port = 6379
#     redis_user = 'r-2zecc8e7087281d4'
#     reids_pwd = 'Bluestackscn2016'
# else:
#     redis_host = 'r-2zecc8e7087281d4.redis.rds.aliyuncs.com'
#     redis_port = 6379
#     redis_user = 'r-2zecc8e7087281d4'
#     reids_pwd = 'Bluestackscn2016'
#
#
# print "redis config:", redis_host,redis_port


#连接时通过password参数指定AUTH信息，由user,pwd通过":"拼接而成
# redis_client = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_user + ':' + reids_pwd)
# redis_client_production = redis.StrictRedis(host=host_production, port=port_production, password=user_production  + ':' + pwd_production)
#
# redis_client = redis.StrictRedis(host=redis_config_test.get("host"), port=redis_config_test.get("port"), password=redis_config_test.get("user") + ':' + redis_config_test.get("pwd"))
# redis_client_production = redis.StrictRedis(host=redis_config_production.get("host"), port=redis_config_production.get("port"), password=redis_config_production.get("user")  + ':' + redis_config_production.get("pwd"))


redis_config_test = {
            "host":'taiwan-test-r.rwrq3m.ng.0001.apn2.cache.amazonaws.com',
            "port":6379,
            "user":'',
            "pwd":''
        }

print redis_client_production

#redis_client = redis.StrictRedis(host=redis_config_test.get("host"), port=redis_config_test.get("port"))


if __name__ == '__main__':
    redis_client.lpush("test_list", "a")
    redis_client.lpush("test_list", "b")
    redis_client.lpush("test_list", "c")

    l = redis_client.llen("test_list")
    while redis_client.llen("test_list") > 0:
        print redis_client.blpop("test_list")

    print redis_client.keys("query_word_*")
    print "---------------------------"
    print redis_client_production.hget("package_user_init","com.huanmeng.zhanjian2")
        # print len(redis_client.keys("test_list"))

    # print redis_client_production.delete("app_center_home@bscn")


#    if redis_client_production.get("app_center_home@bscn"):
#        print json.loads(redis_client_production.get("app_center_home@bscn"))

    #print redis_client.get("app_center_home@koudaibashi")
    #print redis_client.get("app_center_home@xycm")

    #print redis_client.lrange("test_list", 0, 100)






