# -*- coding: utf-8 -*-
"""
    aloneServer
    ~~~~~

    API & Detect Server based on Flask.
    :copyright: (c) 2017 by akasai
"""
from aloneServer.config import *
from aloneServer.util import errLog
from aloneServer.db import connect
from aloneServer.detect import webDetect
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from multiprocessing import Process
from time import ctime

__version__ = '0.3.0'

app = Flask(__name__)
app.config.from_object(DevConfig)
app.secret_key = "secret"
CORS(app)
socketio = SocketIO(app)

class Server(Process):
    from aloneServer import view
    
    def __init__(self):
        Process.__init__(self)
        
    def run(self):
        #Global Singleton Variable Initialize
        logger = errLog.ErrorLog.__call__()
        self.welcomeMSG(logger)
        db = connect.DBConnect.__call__()
        db.setCursor(db.getDB().cursor())
        try:
            WD = webDetect.WebDetect(1,2,3,4)

            socketio.run(app, host="0.0.0.0", port=209)
        except BaseException as s:
            logger.writeLog("critical", "{0} Start Failed. : {1}".format(app, s))

    def welcomeMSG(self, _logger):
        msg  = "********************************************************************\n"
        msg += "*                                                                  *\n"
        msg += "*       PyThOn SeRvEr "+__version__+" StArT "+ctime()+"         *\n"
        msg += "*                                                                  *\n"
        msg += "********************************************************************\n"
        print(msg)
        _logger.writeLog("info", "{0} Start.".format(app))