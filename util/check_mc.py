# # coding=utf-8
# import sys
# import os
# sys.path.append(os.path.dirname(os.path.split(os.path.realpath(__file__))[0]))
# from bst_server.settings import redis_client
#
#
# if __name__ == "__main__":
#     keys = redis_client.keys("to_database:*")
#     for key in keys:
#         count = redis_client.get(key)
#         if int(count) > 1:
#             print key, count
