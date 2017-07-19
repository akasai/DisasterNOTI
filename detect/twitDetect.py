from .config import Key_Config, Keyward
from .listener import Listener
from server import errLog

from multiprocessing import current_process
from tweepy import Stream, OAuthHandler
from tweepy.streaming import StreamListener

def twitDetect(self):
    curProcss = current_process().name
    keyword = []

    for value in Keyward.keywordDic.values():
        for k in value:
            keyword.append(k) 

    auth = OAuthHandler(*Key_Config.consumer)
    auth.set_access_token(*Key_Config.access)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_count=10, retry_delay=5, retry_errors=5)
    l = Listener(self.title, curProcss, self.min_format, keywordDic, self.socketio)

    try: 
        twitterStream = Stream(api.auth, l)
        twitterStream.filter(track=keyword, async=True)
    except BaseException as e:
        errLog.viewLog("error","{0} : Twitter Stream Error".format(e))