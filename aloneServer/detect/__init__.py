#from aloneServer.detect.config import Key_Config, Keyward
from aloneServer.detect import config
from aloneServer.detect import webDetect
'''
from errLog import ErrCon

from .webDetect import webDetect

from .listener import Listener

import multiprocessing
from time import ctime, localtime, sleep
from tweepy import API, Stream, OAuthHandler
from tweepy.streaming import StreamListener
from multiprocessing import Process, current_process
'''


#WD = WebDetect(1,2,3,4)
'''
class WebDetect(Process):
    

    def run(self):
        ErrCon.viewLog("info","{0} - Detecting Start.".format(self.title))
        #print("[{0}]{1} \t- Detecting Start ".format(ctime(),self.title))
        while True:
            try: 
                if localtime().tm_sec == 59:
                    webDetect(self.min_format, self.CONFIG, self.title, self.url)
                    sleep(1)
            except BaseException as e:
                ErrCon.viewLog("error", "WebDetecting Failed. : {0}".format(e))
                break

class TwitDetect(Process):
    def __init__(self, _title, _url, _config, _format):
        Process.__init__(self)
        self.title = _title
        self.url = _url
        self.CONFIG = _config
        self.min_format = _format
    
    def run(self):
        from server import socketio
        curProcss = current_process().name
        keyword = []

        for value in Keyward.keywordDic.values():
            for k in value:
                keyword.append(k) 

        auth = OAuthHandler(*Key_Config.consumer)
        auth.set_access_token(*Key_Config.access)
        api = API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_count=10, retry_delay=5, retry_errors=5)

        l = Listener(self.title, curProcss, self.min_format, Keyward.keywordDic, socketio)
    
        try: 
            twitterStream = Stream(api.auth, l)
            twitterStream.filter(track=keyword, async=True)
        except BaseException as e:
            ErrCon.viewLog("error","{0} : Twitter Stream Error".format(e))
'''