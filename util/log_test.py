# import logging
# import logging.handlers
# import time
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
# logger = logging.handlers.TimedRotatingFileHandler("/mnt/log/preview_bst_server/Rotate_Test.log",'M',1)
# root_logger.addHandler(logger)
#
# while True:
#     daemon_logger = logging.getLogger('TEST')
#     daemon_logger.info("SDFKLDSKLFFJKLSDD")
#     time.sleep(5)