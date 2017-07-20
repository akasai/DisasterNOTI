from .config import Key_Config, Keyward
from .listener import Listener
from server import errLog

from multiprocessing import current_process
from tweepy import API, Stream, OAuthHandler
from tweepy.streaming import StreamListener

def twitDetect(_title, _format, _socketio):
    curProcss = current_process().name
    keyword = []

    for value in Keyward.keywordDic.values():
        for k in value:
            keyword.append(k) 

    #auth = OAuthHandler(*Key_Config.consumer)
    auth = OAuthHandler('445nwUvOWpIfbEAknkSnWW5Bs','jwlX9XxGIXvyZhjquZ8U6JG2yixNhk8btcVW79dMn7mjv5kZgV')
    #auth.set_access_token(*Key_Config.access)
    auth.set_access_token('196210683-AdFNkBpeizJG9dlY1B6uuAjzaTrm23IDz71J1lPV','K8l25sm1QPoxw2T7ow3raSOWNy3R9AasJCELYgnGqfXtk')
    api = API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_count=10, retry_delay=5, retry_errors=5)
    l = Listener(_title, curProcss, _format, Keyward.keywordDic, _socketio)

    try: 
        twitterStream = Stream(api.auth, l)
        twitterStream.filter(track=keyword, async=True)
    except BaseException as e:
        errLog.viewLog("error","{0} : Twitter Stream Error".format(e))
