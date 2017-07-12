from re import sub
from hashlib import md5
from time import time

class Encrypt:
    def keyEncrypt(self,_IP):
        plain_text = int(sub("\.","",str(_IP)))+int(sub("\.","", str(time()))[-12:])
        encrypt = md5(str(plain_text).encode()).hexdigest()        
        return encrypt

ENC = Encrypt()