import requests
from aloneServer.util import errLog
from aloneServer.detect import config
from aloneServer.detect.util import checkCount, isOccur
from bs4 import BeautifulSoup
from multiprocessing import Process, current_process
from time import localtime, ctime, strftime, sleep

logger = errLog.ErrorLog.__call__()

class NewsDetect(Process):
    def __init__(self, _title, _url, _config, _format):
        Process.__init__(self)
        self.title = _title
        self.url = _url
        self.CONFIG = _config
        self.min_format = _format
        self.tmp_cnt = 0

    def run(self):
        logger.writeLog("info","{0} - Detecting Start.".format(self.title))
        while True:
            try:
                if localtime().tm_sec == 15 or localtime().tm_sec == 45:
                    self.detect(self.CONFIG, self.title, self.url)
                    sleep(1)
            except BaseException as e:
                logger.writeLog("error", "NEWS Detecting Failed. : {0}".format(e))
                break

    def detect(self, _config, _title, _url):
        curProcss = current_process().name

        try:
            source_code = requests.get(_url)
            soup = BeautifulSoup(source_code.text, "html.parser")

            for s in soup.select(_config['className']):
                cnt = s.text[7:-1].replace(",","")

        except BaseException as e:
            logger.writeLog("error", "{0} - NEWS Detecting Stoped. : {1}".format(_title, e))
        else:
            gap = self.tmp_cnt-int(cnt)
            print("[{0}] {1}-{2}\t{3} ".format(ctime(), curProcss, _title, checkCount(gap, "", "뉴스")))
            self.tmp_cnt = int(cnt)
            #logger.writeLog("info","{0}\t{1} ".format(_title, checkCount(lastest_num, _title, "지진")))