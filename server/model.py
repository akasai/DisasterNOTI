class tokenSelect:
    def __init__(self, _cursor, _ip="%"):
        self.query = "select ip, AES_DECRYPT(UNHEX(accessKey), 'acorn') from tb_access_auth where ip='"+_ip+"';"
        self.cur = _cursor
        self.cur.execute(self.query)
        self.isEmpty(self.cur.fetchone())
    
    def isEmpty(self, _row):
        if _row:    #값이 있으면
            self.ip = self.cur.fetchone()[0]
            self.key = self.cur.fetchone()[1]
        else:       #값이 없으면
            self.ip = None
            self.key = None

    def __repr__(self):
        return "{0}".format(self.key)
        #return "{0} - {1}".format(self.ip, self.key)