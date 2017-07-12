from server import app

#import logging
from logging.handlers import RotatingFileHandler
from logging import Formatter

fileMaxByte = 1024 * 1024 * 100 #100MB
fomatter = Formatter('[%(asctime)19s] [%(levelname)8s] [%(processName)12s] - %(message)s')

fileHandler = RotatingFileHandler('./log/serverLog.log', maxBytes=fileMaxByte, backupCount=10, encoding="utf-8")
fileHandler.setFormatter(fomatter)

'''
기존 app.logger 의 Stream을 사용
streamHandler = logging.StreamHandler()
streamHandler.setFormatter(fomatter)
app.logger.addHandler(streamHandler) 
'''

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
    app.logger.handlers[0].setFormatter(fomatter)
    
    app.logger.setLevel(level)
    
def viewLog(mode, msg=None):
    '''
    전달 mode에 따라 logging.
    ''' 
    if mode is "critical":
        print()
        app.logger.critical(msg)
        print()
    elif mode is "error":
        print()
        app.logger.warning(msg)
        print()
    elif mode is "warning":
        print()
        app.logger.warning(msg)
        print()
    elif mode is "info":
        print()
        app.logger.info(msg)
        print()
       
    '''
    if mode is "message":
        app.logger.info("[message] user_key : {}, type : {}, content : {}".format(
            data["user_key"],
            data["type"],
            data["content"]))
    
    elif mode is "add":
        app.logger.info("[join] user_key : {}".format(data["user_key"]))
    elif mode is "block":
        app.logger.info("[block] user_key : {}".format(data))
    elif mode is "exit":
        app.logger.info("[exit] user_key : {}".format(data))
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