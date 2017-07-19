import MySQLdb
from flask import Flask
from flask_cors import CORS
from time import ctime
from multiprocessing import Process
from .config import DB_Config

#Flask initialize
app = Flask(__name__)
CORS(app)
app.config.from_object(config.DevConfig)

#ErrorModule import
from server import errLog
errLog.setLogger(app,10)

#DB Connect & model initialize
try:
    db = MySQLdb.connect(**DB_Config.db_config)
    
    errLog.viewLog("info", "{0} Connected".format(db))
except BaseException as b:
    errLog.viewLog("critical", b)
finally:
    from server import view

 
from detect import Init, twitDetect


#server Initialize -> log 남기기
def serverStart():
    msg  = "********************************************************************\n"
    msg += "*                                                                  *\n"
    msg += "*                                                                  *\n"
    msg += "*                                                                  *\n"
    msg += "*          PyThOn SeRvEr StArT "+ctime()+"            *\n"
    msg += "*                                                                  *\n"
    msg += "*                                                                  *\n"
    msg += "*                                                                  *\n"
    msg += "********************************************************************\n"
    print(msg)
    #app.run(host='0.0.0.0', debug = False, port=209, threaded=True)
    #socketio.run(app, host='0.0.0.0', port=209)
    #Process(targ et = socketio.run(app, host='0.0.0.0', port=209), name = 'ServertProcess', threaded=True).start()
    Process(target = app.run(host='0.0.0.0', port=209), name = 'ServertProcess', threaded=True).start()
    
