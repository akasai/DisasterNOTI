import requests
import json

from aloneServer.util import errLog
from flask import abort
from re import sub, compile
from hashlib import md5
from time import time, ctime

logger = errLog.ErrorLog.__call__()

def HTTPError(_statusCode, _msg, _ip=None):
    logger.writeLog("warning", "[{0}]{1} : {2}".format(_statusCode, _msg, _ip))
    return abort(_statusCode, 'Access Denied. '+str(_msg))

class Tool():
    def setRespJson(self, _uri, _output):
        result = []
        url = _uri
        source = requests.get(url).json()
        s = str(source['rtn_result'])

        if s == None:
            logger.writeLog("info", 'No Data')
            return False
    
        plain_text = s.split('||')
        c = compile(r"(\d+).(\d+),(.?\d+)")
        met = c.findall(plain_text[0])
    
        for a in met:
            timestamp = a[0]+""+a[1][:3]
            data = {"time":int(timestamp),"value":str(a[2])}
            result.append(data)
    
        sortedResult = sorted(result, key=self.getTime, reverse=False)
        _output.put(json.dumps(sortedResult))

    def getTime(self, _n):
        return int(_n.get('time'))

class Encrypt:
    def keyEncrypt(self,_IP):
        plain_text = int(sub("\.","",str(_IP)))+int(sub("\.","", str(time()))[-12:])
        encrypt = md5(str(plain_text).encode()).hexdigest()        
        return encrypt

