from server import app
from logging.handlers import RotatingFileHandler
from logging import Formatter

fileMaxByte = 1024 * 1024 * 100 #100MB
fomatter = Formatter('[%(asctime)19s] [%(levelname)8s] [%(processName)12s] - %(message)s')#추후 변경

fileHandler = RotatingFileHandler('./log/serverLog.log', maxBytes=fileMaxByte, backupCount=10, encoding="utf-8")
fileHandler.setFormatter(fomatter)
processfileHandler = RotatingFileHandler('./log/processLog.log', maxBytes=fileMaxByte, backupCount=10, encoding="utf-8")
processfileHandler.setFormatter(fomatter)

#Singleton class
class SingletonType(type):
    def __call__(_cls, *args, **kwargs):
        try:
            return _cls.__intsance
        except AttributeError:
            _cls.__instance = super(SingletonType, _cls).__call__(*args, **kwargs)
            return _cls.__instance

class ErrLog(metaclass=SingletonType):
    def setProcessLogger(self,_logger, level):
        logger =_logger
        logger.setLevel(level)
        logger.addHandler(processfileHandler)

    def setLogger(self, app, level):
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
    
    def viewLog(self, mode, msg=None):
        '''
        전달 mode에 따라 logging.
        critical : 서버운영에 지장을 주는 정도
        error : 서버운영은 유지되지만 기능에 지장이 생기는 정도
        warning : 서버운영은 유지되지만 기능적 제한이 생기는 정도
        info : 서버운영 알림
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