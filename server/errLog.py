import logging
from logging.handlers import RotatingFileHandler
#from logging import Formatter

from server import app

import os
import time

#logger = logging.getLogger('mylogger')

fileMaxByte = 1024 * 1024 * 100 #100MB

fomatter = logging.Formatter('%(asctime)19s  %(levelname)8s [%(filename)s:%(lineno)s] %(processName)13s  %(message)s')

fileHandler = RotatingFileHandler('./log/serverLog.log', maxBytes=fileMaxByte, backupCount=10, encoding="utf-8").setFormatter(fomatter)
streamHandler = logging.StreamHandler().setFormatter(fomatter)


def setLogger(app, level):
    '''
    Level	    Numeric value
    CRITICAL	50
    ERROR	    40
    WARNING	    30
    INFO	    20
    DEBUG	    10
    NOTSET	    0
    '''
    app.logger.addHandler(fileHandler)
    app.logger.addHandler(streamHandler) 

    app.logger.setLevel(level)

def viewLog(mode, msg):
    '''
    전달 mode에 따라 logging.
    '''
    if mode is "error":
        app.logger.error()
    '''
    if mode is "message":
        app.logger.info("[message] user_key : {}, type : {}, content : {}".format(
            data["user_key"],
            data["type"],
            data["content"]))
    elif mode is "keyboard":
        app.logger.info("[keyboard] call home keyboard")
    elif mode is "add":
        app.logger.info("[join] user_key : {}".format(data["user_key"]))
    elif mode is "block":
        app.logger.info("[block] user_key : {}".format(data))
    elif mode is "exit":
        app.logger.info("[exit] user_key : {}".format(data))
    elif mode is "fail":
        app.logger.info("[fail] request process fail")
    '''
'''
logger.setLevel(logging.DEBUG)
logger.debug("===========================")
logger.info("TEST START")
logger.warning("스트림으로 로그가 남아요~")
logger.error("파일로도 남으니 안심이죠~!")
logger.critical("치명적인 버그는 꼭 파일로 남기기도 하고 메일로 발송하세요!")
logger.debug("===========================")
'''