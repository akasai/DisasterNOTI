import requests
from bs4 import BeautifulSoup

from multiprocessing import current_process
from time import localtime, ctime, strftime#, strptime, sleep, ctime, time
from .Tool import _get_article_Time, checkCount

def webDetect(_minFormat, _config, _title, _url):
    lastest_num = 0
    creteria = strftime(_minFormat, localtime())
    curProcss = current_process().name
    try:
        source_code = requests.get(_url)
        plain_code = source_code.text
        soup = BeautifulSoup(plain_code, "html.parser")
        
        for target_text in soup.select(_config['rowName']):
            if _get_article_Time(target_text, _config, _minFormat) == creteria: #_creteria:
                lastest_num += 1
        
        print("[{0}] {1}-{2}\t{3} ".format(ctime(), curProcss, _title, checkCount(lastest_num, _title, "지진")))
    except BaseException as e:
        ErrCon.viewLog("error", "{0} - WebDetecting Stoped. : {1}".format(_title, e))
        #print("[{0}]{1} \t- Detecting Stoped \t{2}".format(ctime(), _title, e))