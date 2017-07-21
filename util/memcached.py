#coding=utf-8

#import memcache
import os
import sys
import bmemcached

sys.path.append(os.path.dirname(os.path.split(os.path.realpath(__file__))[0]))

from bst_android_market.settings import ENVIRONMENT, mc_client

#from bst_server.settings import ALIYUN_MEMCACHE_HOST,ALIYUN_MEMCACHE_USERNAME,ALIYUN_MEMCACHE_PASSWORD,ENVIRONMENT,USE_MC_ENVIRONMENT, \
#    ALIYUN_MEMCACHE_PREVIEW_HOST, ALIYUN_MEMCACHE_PREVIEW_USERNAME, ALIYUN_MEMCACHE_PREVIEW_PASSWORD


# if (ENVIRONMENT in USE_MC_ENVIRONMENT) and ENVIRONMENT == "aliyun":   #正式环境
#
#     mc_client = bmemcached.Client((ALIYUN_MEMCACHE_HOST,),
#                                    ALIYUN_MEMCACHE_USERNAME,
#                                    ALIYUN_MEMCACHE_PASSWORD)
# elif (ENVIRONMENT in USE_MC_ENVIRONMENT) and ENVIRONMENT == "aliyun_test_preview":     #预发环境
#     mc_client = bmemcached.Client((ALIYUN_MEMCACHE_PREVIEW_HOST,),
#                                    ALIYUN_MEMCACHE_PREVIEW_USERNAME,
#                                    ALIYUN_MEMCACHE_PREVIEW_PASSWORD)
# else: #默认使用aliyun环境的
#     mc_client = bmemcached.Client((ALIYUN_MEMCACHE_HOST,),
#                                    ALIYUN_MEMCACHE_USERNAME,
#                                    ALIYUN_MEMCACHE_PASSWORD)


#
# if __name__ == '__main__':
#     a = AliyunMemcached()
#     AliyunMemcached.mgr().set("abc", "cba", time=3600)
#
#from bluestacks.models import MCClient
#正式
#mc_client = bmemcached.Client(("da9b304ea6e0492b.m.cnbjalinu16pub001.ocs.aliyuncs.com:11211",),
#                               "da9b304ea6e0492b",
#                               "Bluestacks2016")
# 预发
# mc_client = bmemcached.Client(("ec8c5722e776438c.m.cnbjalinu16pub001.ocs.aliyuncs.com:11211",),
#                               "ec8c5722e776438c",
#                               "Bluestacks2016")


# 台湾预发 
#mc_client = bmemcached.Client(("taiwan-test.rwrq3m.cfg.apn2.cache.amazonaws.com:11211",),
#                               "",
#                               "")

# mc_client = bmemcached.Client(("taiwan-production.rwrq3m.cfg.apn2.cache.amazonaws.com:11211",),
#                                "",
#                                "")

#win test


#print mc_client.flush_all()

#print MCClient.get("get_useful_partner")
a = mc_client.delete("check_package_name@com.netease.onmyoji.uc@bscn")
print a


#print mc_client.delete("abc")



