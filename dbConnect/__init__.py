import MySQLdb
from server.config import DB_Config
from errLog import ErrCon

try:
    db = MySQLdb.connect(**DB_Config.db_config)
    ErrCon.viewLog("info", "{0} Connected.".format(db))
except BaseException as b:
    ErrCon.viewLog("critical", b)