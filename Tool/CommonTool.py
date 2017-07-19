import requests
import json

from server import errLog
from re import sub, compile
from hashlib import md5
from time import time, ctime

def setRespJson(_uri, _output):
    result = []
    url = _uri
    source = requests.get(url).json()
    s = str(source['rtn_result'])

    if s == None:
        errLog.viewLog("info", 'No Data')
        return False
    
    plain_text = s.split('||')
    c = compile(r"(\d+).(\d+),(.?\d+)")
    met = c.findall(plain_text[0])
    
    for a in met:
        timestamp = a[0]+""+a[1][:3]
        data = {"time":int(timestamp),"value":str(a[2])}
        result.append(data)
    
    sortedResult = sorted(result, key=getTime, reverse=False)
    _output.put(json.dumps(sortedResult))

def getTime(_n):
    return int(_n.get('time'))

class Encrypt:
    def keyEncrypt(self,_IP):
        plain_text = int(sub("\.","",str(_IP)))+int(sub("\.","", str(time()))[-12:])
        encrypt = md5(str(plain_text).encode()).hexdigest()        
        return encrypt

ENC = Encrypt()