#from server import app

import logging
from .config import format_Config
from logging.handlers import RotatingFileHandler
from logging import Formatter

#Singleton class
class SingletonType(type):
    def __call__(_cls, *args, **kwargs):
        try:
            return _cls.__intsance
        except AttributeError:
            _cls.__instance = super(SingletonType, _cls).__call__(*args, **kwargs)
            return _cls.__instance

class ErrLog(object):
    __metaclass__ = SingletonType
    _logger = None
    #_plogger = None
    def __init__(self, _test):
        print(_test)
        self._logger = logging.getLogger("testlogger")
     #   self._plogger = logging.getLogger("testlogger2")
        
        self._logger.setLevel(10)
      #  self._plogger.setLevel(10)

        fileHandler = logging.FileHandler(**format_Config.serverLog)
        fileHandler.setFormatter(Formatter(format_Config.server_format))
        pHandler = logging.FileHandler(**format_Config.procLog)
        pHandler.setFormatter(Formatter(format_Config.proc_format))

        self._logger.addHandler(fileHandler)
       # self._plogger.addHandler(pHandler)

        #self.fileHandler = RotatingFileHandler(**format_Config.serverLog)
        #self.fileHandler.setFormatter(Formatter(format_Config.server_format))
        #self.detectHandler = RotatingFileHandler(**format_Config.detectLog)
        #self.detectHandler.setFormatter(Formatter(format_Config.detect_format))
        #self.processfileHandler = RotatingFileHandler(**format_Config.procLog)
        #self.processfileHandler.setFormatter(Formatter(format_Config.proc_format))
        

        #app.logger.addHandler(self.fileHandler)
        #app.logger.handlers[0].setFormatter(Formatter(format_Config.stream_format))
        #app.logger.handlers[1].setFormatter(Formatter(format_Config.stream_format))   
        
    def setProcessLogger(self,_logger, level):
        logger =_logger
        logger.setLevel(level)
        logger.addHandler(self.processfileHandler)
    
    def setDetectLogger(self,_logger, level):
        logger =_logger
        logger.setLevel(level)
        logger.addHandler(self.processfileHandler)

    def setLogger(self, level):
        '''
        Level	    Numeric value
        CRITICAL	50
        ERROR	    40
        WARNING	    30
        INFO	    20
        DEBUG	    10
        NOTSET	    0
        '''
        app.logger.setLevel(level)
    
    def getLogger(self):
        return self._logger

    def getPLogger(self):
        return self._plogger

    def viewLog(self, mode, msg=None):
        '''
        전달 mode에 따라 logging.
        critical : 서버운영에 지장을 주는 정도
        error : 서버운영은 유지되지만 기능에 지장이 생기는 정도
        warning : 서버운영은 유지되지만 기능적 제한이 생기는 정도
        info : 서버운영 알림
        ''' 
        if mode is "critical":
            app.logger.critical(msg)
        elif mode is "error":
            app.logger.warning(msg)
        elif mode is "warning":
            app.logger.warning(msg)
        elif mode is "info":
            app.logger.info(msg)