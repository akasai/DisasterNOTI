import MySQLdb
from flask import Flask
from flask_cors import CORS
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