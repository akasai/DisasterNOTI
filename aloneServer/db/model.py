from aloneServer.util import errLog
from aloneServer.db import connect
from aloneServer.db.message import SuccessMessage, FailMessage

logger = errLog.ErrorLog.__call__()
db = connect.DBConnect.__call__()

class tokenSelect:
    def __init__(self, _ip="%"):
        self.query = "select ip, AES_DECRYPT(UNHEX(accessKey), 'acorn') from tb_access_auth where ip like '"+_ip+"';"
        self.cur = db.getCursor()
        try:
            self.cur.execute(self.query)
            self.isEmpty(self.cur.fetchone())
        except BaseException as e:
            logger.writeLog("error","Token Select Failed. : {0}".format(e))
    
    def isEmpty(self, _row):
        if _row:    #값이 있으면
            self.ip = _row[0]
            self.key = _row[1].decode()
        else:       #값이 없으면
            self.ip = None
            self.key = None

    def __repr__(self):
        return "{0}".format(self.key)

class tokenInsert:
    def __init__(self, _userIP, _encryptKey):
        self.query = "insert into tb_access_auth values ('"+_userIP+"',HEX(AES_ENCRYPT('"+_encryptKey+"','acorn')),sysdate(),'on');"
        self.cur = db.getCursor()

        try:
            self.cur.execute(self.query)
            self.returnMsg = SuccessMessage().getMessage()
        except BaseException as e:
            logger.writeLog("error", "Token Insert Error. : {0}".format(e))
            self.returnMsg = FailMessage().getMessage()
        else:
            logger.writeLog("info", "Token Commit Success.")
            db.getDB().commit()

    def __repr__(self):
        return self.returnMsg

class ValidSelect:
    def __init__(self, _accessKey):
        self.query = "select * from tb_access_auth where accessKey = HEX(AES_ENCRYPT('"+_accessKey+"','acorn'));"
        self.cur = db.getCursor()

        try:
            self.cur.execute(self.query)
            self.isEmpty(self.cur.fetchone())
        except BaseException as e:
            logger.writeLog("error", "Vailed Select Failed. : {0}".format(e))
        
    def isEmpty(self, _row):
        if _row:    #값이 있으면
            self.returnMsg = SuccessMessage().getMessage()
        else:       #값이 없으면
            self.returnMsg = FailMessage().getMessage()

    def __repr__(self):
        return self.returnMsg