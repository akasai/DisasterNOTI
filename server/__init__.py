import multiprocessing
from .config import DevConfig

from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from multiprocessing import Process
from time import ctime

app = Flask(__name__)
app.config.from_object(DevConfig)
app.secret_key = "secret"
CORS(app)
socketio = SocketIO(app)

from server import view
#ErrorModule import
from errLog import ErrCon
ErrCon.setLogger(10)
    
class Server(Process):
    def __init__(self):
        Process.__init__(self)
        
    #Flask initialize
    def run(self):
        from dbConnect import db
        #multiprocessing.log_to_stderr()
        ErrCon.setProcessLogger(multiprocessing.get_logger(), 10)
        try:
            self.welcomeMSG()
            socketio.run(app, host="0.0.0.0", port=209)    
        except Exception as e:
            ErrCon.viewLog("critical", "{0} Start Failed. : {1}".format(app, e))
    
    #server Initialize    
    def welcomeMSG(self):
        msg  = "********************************************************************\n"
        msg += "*                                                                  *\n"
        msg += "*          PyThOn SeRvEr StArT "+ctime()+"            *\n"
        msg += "*                                                                  *\n"
        msg += "********************************************************************\n"
        ErrCon.viewLog("info", "{0} Start.".format(app))
        print(msg)
'''
from .config import Detect_Config
from detect import Detect, twitDetect
#m  = Detect(**CONFIG3)
#c  = Detect(**CONFIG2)
'''