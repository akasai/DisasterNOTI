import MySQLdb
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from time import ctime
from multiprocessing import Process
from .config import DB_Config, Detect_Config

#Flask initialize
app = Flask(__name__)
app.config.from_object(config.DevConfig)
app.secret_key = "secret"
CORS(app)
socketio = SocketIO(app)

#ErrorModule import
from server import errLog
errLog.setLogger(app,10)

#DB Connect & model initialize
try:
    db = MySQLdb.connect(**DB_Config.db_config)    
    errLog.viewLog("info", "{0} Connected.".format(db))
except BaseException as b:
    errLog.viewLog("critical", b)
finally:
    from server import view
    from detect import Detect, twitDetect

#m  = Detect(**CONFIG3)
#c  = Detect(**CONFIG2)

#server Initialize
def serverStart():
    msg  = "********************************************************************\n"
    msg += "*                                                                  *\n"
    msg += "*          PyThOn SeRvEr StArT "+ctime()+"            *\n"
    msg += "*                                                                  *\n"
    msg += "********************************************************************\n"
   
    try:
        print(msg)
        errLog.viewLog("info", "{0} Start.".format(app))
        Process(target=socketio.run(app, host='0.0.0.0', port=209), name='ServerProcess', threaded=True).start()
    except BaseException as e:
        print(e)
        errLog.viewLog("critical", "{0} Start Failed. : {1}".format(app, e))
