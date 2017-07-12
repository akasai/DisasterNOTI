from server import errLog
'''
superclass로 각각의 벨류 뽑는 클래스 만들기
ex) "success" 가 STR이 아니라 각각의 클래스 type으로 return

'''
class tokenSelect:
    def __init__(self, _cursor, _ip="%"):
        self.query = "select ip, AES_DECRYPT(UNHEX(accessKey), 'acorn') from tb_access_auth where ip like'"+_ip+"';"
        self.cur = _cursor
        self.cur.execute(self.query)
        self.isEmpty(self.cur.fetchone())
    
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
    def __init__(self, _cursor, _userIP, _encryptKey):
        self.query = "insert into tb_access_auth values ('"+_userIP+"',HEX(AES_ENCRYPT('"+_encryptKey+"','acorn')),sysdate(),'on');"
        self.cur = _cursor
        try:
            self.cur.execute(self.query)
            self.returnMsg = "success"
        except BaseException as e:
            errLog.viewLog("error", e)
            self.returnMsg = "fail"

    def __repr__(self):
        return self.returnMsg
