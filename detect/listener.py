from errLog import ErrCon

from .Tool import *

import json
from time import strptime, ctime, time
from datetime import datetime, timedelta
from tweepy.streaming import StreamListener

class Listener(StreamListener):
    def __init__(self, _title, _process, _format, _keywordDic, _sock):
        self.title = _title
        self.curProcess = _process
        self.format = _format
        self.tmp_time = time()
        self.sockio = _sock 

        self.keywordDic = _keywordDic
        self.counting = setInitial(self.keywordDic)

    def on_connect(self):
        ErrCon.viewLog("info","{0} - Detecting Start.".format(self.title))
        #print("[{0}]{1} \t- Detecting Start ".format(ctime(),self.title))
    
    def on_data(self, raw_data):
        data = json.loads(raw_data)
        
        utctime = datetime.strptime(data['created_at'], self.format)
        kor_time = utctime + timedelta(hours=9)

        if 'retweeted_status' in data:
            pass
        else:
            for i, k in enumerate(self.keywordDic.values()):
                for value in k:
                    if value in data['text']:
                        setCounting(self.counting, i)

                if isOneMin(self.tmp_time):
                    for k in self.counting:
                        print("[{0}] {1}-{2}({3})\t{4}".format(ctime(), self.curProcess, self.title, k, checktwitCount(self.sockio, self.counting.get(k), k, self.tmp_time)))
                    self.tmp_time = time()
                    resetCount(self.counting)

    def keep_alive(self):
        try:
            pass
        except ConnectionAbortedError as c:
            ErrCon.viewLog("info","{0} - Detecting Stoped. : {1}".format(self.title, c))
            #print("[{0}]{1} \t- Detecting Stoped \t{2}".format(ctime(), self.title, c))

    def on_error(self, _status):
        ErrCon.viewLog("error","Twitter Detecting Error. : {0}".format(_status))
        #print(_status)