from time import ctime, localtime, sleep
from .twitDetect import twitDetect
from .webDetect import webDetect

class Detect:
    def __init__(self, _title, _url, _config, _format):
        self.title = _title
        self.url = _url
        self.CONFIG = _config
        self.min_format = _format

    def webDetecting(self):
        print("[{0}]{1} \t- Detecting Start ".format(ctime(),self.title))
        while True:
            try: 
                if localtime().tm_sec == 59:
                    webDetect(self.min_format, self.CONFIG, self.title, self.url)
                    sleep(1)
            except BaseException as e:
                print(e)
                break
    
    def twitDetecting(self, _sock=None):
        self.socketio = _sock
        twitDetect(self.title, self.min_format, self.socketio)  
        