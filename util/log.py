# # coding=utf-8
#
# import logging
# import logging.handlers
#
# import time
#
# from bst_server.settings import ENVIRONMENT
#
# LOGGING_MSG_FORMAT  = '%(name)-14s > [%(levelname)s] [%(asctime)s] : %(message)s'
# LOGGING_DATE_FORMAT	= '%Y-%m-%d %H:%M:%S'
#
# logging.basicConfig(
#             level=logging.DEBUG,
#             format=LOGGING_MSG_FORMAT,
#             datefmt=LOGGING_DATE_FORMAT
#             )
# root_logger = logging.getLogger('')
# log_dir = "/mnt/log/Rotate_Test.log"
# if ENVIRONMENT == "win_test":
#     log_dir = "../Rotate_Test.log"
# elif ENVIRONMENT == "aliyun_test_preview":
#     log_dir = "/mnt/log/preview_bst_server/Rotate_Test.log"
#
# handler = logging.handlers.TimedRotatingFileHandler(log_dir,'M',1)
# root_logger.addHandler(handler)
#
# # daemon_logger = logging.getLogger('bst')