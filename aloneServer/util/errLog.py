# -*- coding: utf-8 -*-
"""
    util Logging
    ~~~~~~~~~~~~~~
    
    Singleton pattern Class
    logging class based on logging
"""
import logging
from logging import Formatter
from logging.handlers import RotatingFileHandler

#Singleton class
class SingletonType(type):
    #__intsance = None
    def __call__(_cls, *args, **kwargs):
        try:
            return _cls.__intsance
        except AttributeError:
            _cls.__instance = super(SingletonType, _cls).__call__(*args, **kwargs)
            return _cls.__instance

class ErrorLog(metaclass=SingletonType):
    #Logger Variable
    _logger = None

    def __init__(self):
        self._logger = logging.getLogger("serverLogger")

    def setLogger(self, _lv):
        self._logger.setLevel(_lv)

    def getLogger(self):
        return self._logger