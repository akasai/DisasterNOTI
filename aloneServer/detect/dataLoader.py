import requests
from aloneServer.util import errLog
from aloneServer.detect.util import _get_article_Time, checkCount
from bs4 import BeautifulSoup
from multiprocessing import Process, current_process
from time import localtime, ctime, strftime, sleep

logger = errLog.ErrorLog.__call__()

class DataLoader(Process):
    def __init__(self, _title, _url, _config, _format):
        Process.__init__(self)
        self.title = _title
        self.url = _url
        self.CONFIG = _config
        self.min_format = _format

    def run(self):
        logger.writeLog("info","{0} - Detecting Start.".format(self.title))
        while True:
            try:
                if localtime().tm_sec == 59:
                    self.detect(self.min_format, self.CONFIG, self.title, self.url)
                    sleep(1)
            except BaseException as e:
                logger.writeLog("error", "WebDetecting Failed. : {0}".format(e))
                break

    def detect(self, _minFormat, _config, _title, _url):
        lastest_num = 0
        creteria = strftime(_minFormat, localtime())
        curProcss = current_process().name
        
        try:
            source_code = requests.get(_url)
            plain_code = source_code.text
            soup = BeautifulSoup(plain_code, "html.parser")
            
            for target_text in soup.select(_config['rowName']):
                if _get_article_Time(target_text, _config, _minFormat) == creteria:
                    lastest_num += 1
        except BaseException as e:
            logger.writeLog("error", "{0} - WebDetecting Stoped. : {1}".format(_title, e))
        else:
            #logger.writeLog("info","{0}\t{1} ".format(_title, checkCount(lastest_num, _title, "지진")))
            print("[{0}] {1}-{2}\t{3} ".format(ctime(), curProcss, _title, checkCount(lastest_num, _title, "지진")))
"""

@app.route('/sample')
def sample():
    db = MySQLdb.connect(host=dbServer,port=port,user="root",passwd="1111",db="test", charset='utf8')
    cursor = db.cursor()
    query = "select max(eqid) from tb_earthquake_fast;"
    cursor.execute(query)
    rows = cursor.fetchone()

    if rows[0] == None:
        cnt = 1
    else:
        cnt = int(rows[0])+1

    try:
        date1 = "1978"#1978~2017
        callback = request.args.get('callback')
        ori_url = "http://www.kma.go.kr"
        

        for d in range(2017, 2018):
            date = str(d)
            r_page = getRelativePage(date)
            sleep(1)
            maxpage = getOriginPage(date) 
            sleep(1)
            print("{0} StartTime time {1}".format(date, ctime()))
            for pa in range(0, maxpage):
                url = ori_url + "/weather/earthquake_volcano/domesticlist.jsp?startSize=0&endSize=10&pNo="+str(pa+1)+"&startTm=" + str(date + "-01-01") + "&endTm=" + str(date + "-12-31")
                source = requests.get(url)
                soup =  BeautifulSoup(source.text, 'html.parser')
                begin = 0
                for s in soup.select('table.table_develop > tbody > tr'):
                    if not _get_Time(s) == None:
                        try:
                            data = {'time':_get_Time(s),'degree':_get_Degree(s),'title':_get_Title(s),'lat':_get_Lat(s).strip(),'lng':_get_Lng(s).strip(),'tag': _get_Tag(ori_url,s)}
                    
                            for b in range(begin, r_page):
                                stoper = spider(b+1, _get_Time(s), date, data)
                                if stoper:
                                    break
                        except BaseException as e:
                            print("semi : ",e)
                        finally:
                            data['eqid'] = cnt
                            columns = ','.join(data.keys())
                            placeholders = ','.join(['%s'] * len (data))
                            query = "insert into tb_earthquake_fast ({0}) values ({1})".format(columns, placeholders)
                            try:
                                cursor.execute(query, data.values())
                                print("Processing {0} {1}".format(cnt,ctime()))
                                cnt += 1
                            except BaseException as e:
                                print("inner : ",e)
            print("{0} End time {1}".format(date, ctime()))
    except BaseException as e:
        print("outter :", e)
    finally:
        db.commit()
        db.close()
        print("All End time {0}".format(ctime()))
    return 'test'


def spider(_page, _time, _year, _data):
    url = "http://necis.kma.go.kr/necis-dbf/user/earthquake/annual_earthquake_list.do?pageIndex="+str(_page)+"&cal_url=%2Fnecis-dbf%2Fsym%2Fcal%2FEgovNormalCalPopup.do&closeYnCheck=&pSort=&pOrderBy=&locationCheckBox=%EC%84%9C%EC%9A%B8&locationCheckBox=%EA%B2%BD%EA%B8%B0&locationCheckBox=%EC%9D%B8%EC%B2%9C&locationCheckBox=%EB%B6%80%EC%82%B0&locationCheckBox=%EA%B2%BD%EB%82%A8&locationCheckBox=%EC%9A%B8%EC%82%B0&locationCheckBox=%EB%8C%80%EA%B5%AC&locationCheckBox=%EA%B2%BD%EB%B6%81&locationCheckBox=%EA%B4%91%EC%A3%BC&locationCheckBox=%EC%A0%84%EB%82%A8&locationCheckBox=%EC%A0%84%EB%B6%81&locationCheckBox=%EB%8C%80%EC%A0%84&locationCheckBox=%EC%B6%A9%EB%82%A8&locationCheckBox=%EC%B6%A9%EB%B6%81&locationCheckBox=%EA%B0%95%EC%9B%90&locationCheckBox=%EC%A0%9C%EC%A3%BC&locationCheckBox=%EB%B6%81%ED%95%9C&locationCheckBox=%EA%B8%B0%ED%83%80&seaCheckBox=130&seaCheckBox=110&seaCheckBox=120&magnitudeFrom=&magnitudeTo=&latitudeFrom=&latitudeTo=&longitudeFrom=&longitudeTo=&stdYear="+str(_year)+"&endYear="+str(_year)+"&searchWord="
    source_code = requests.get(url)
    soup = BeautifulSoup(source_code.text, 'html.parser')
    for tr in soup.select('table.obsTable tbody tr'):
        if _get_target_time(tr) == _time:
            _data['url'] = _get_pulse_url(tr)
            return True
        else:
            _data['url'] = ""

def getOriginPage(_year):
    page_url = "http://www.kma.go.kr/weather/earthquake_volcano/domesticlist.jsp?startSize=0&endSize=10&pNo=1&startTm=" + str(_year + "-01-01") + "&endTm=" + str(_year + "-12-31")
    page_source = requests.get(page_url)
    p_soup =  BeautifulSoup(page_source.text, 'html.parser')
    
    for t in p_soup.select('span.last > a'):
            p = t['href']
            c = re.compile(r"(pNo=\d+)")
            a = c.findall(p)
            page = int(a[0][4:])
    return page

def getRelativePage(_year):
    url = "http://necis.kma.go.kr/necis-dbf/user/earthquake/annual_earthquake_list.do?pageIndex=1&cal_url=%2Fnecis-dbf%2Fsym%2Fcal%2FEgovNormalCalPopup.do&closeYnCheck=&pSort=&pOrderBy=&locationCheckBox=%EC%84%9C%EC%9A%B8&locationCheckBox=%EA%B2%BD%EA%B8%B0&locationCheckBox=%EC%9D%B8%EC%B2%9C&locationCheckBox=%EB%B6%80%EC%82%B0&locationCheckBox=%EA%B2%BD%EB%82%A8&locationCheckBox=%EC%9A%B8%EC%82%B0&locationCheckBox=%EB%8C%80%EA%B5%AC&locationCheckBox=%EA%B2%BD%EB%B6%81&locationCheckBox=%EA%B4%91%EC%A3%BC&locationCheckBox=%EC%A0%84%EB%82%A8&locationCheckBox=%EC%A0%84%EB%B6%81&locationCheckBox=%EB%8C%80%EC%A0%84&locationCheckBox=%EC%B6%A9%EB%82%A8&locationCheckBox=%EC%B6%A9%EB%B6%81&locationCheckBox=%EA%B0%95%EC%9B%90&locationCheckBox=%EC%A0%9C%EC%A3%BC&locationCheckBox=%EB%B6%81%ED%95%9C&locationCheckBox=%EA%B8%B0%ED%83%80&seaCheckBox=130&seaCheckBox=110&seaCheckBox=120&magnitudeFrom=&magnitudeTo=&latitudeFrom=&latitudeTo=&longitudeFrom=&longitudeTo=&stdYear="+str(_year)+"&endYear="+str(_year)+"&searchWord="
    source_code = requests.get(url)
    soup = BeautifulSoup(source_code.text, 'html.parser')
    
    if not len(soup.select('div.pagination > a')) == 0:
        for a in soup.select('div.pagination > a'):
            c = re.compile(r"(\d+)")
            p = c.findall(a['href'])
            page = int(p[0])
    else:
        page = 1
    
    return page

def _get_Time(_plainText):
    #for td in _plainText.select('td:nth-of-type(2)'):
    for i, td in enumerate(_plainText.select('td')):
        if i == 1:
            try:
                return strftime('%Y-%m-%d %H:%M:%S', strptime(td.text, '%Y/%m/%d %H:%M:%S'))
            except:
                return None

def _get_Degree(_plainText):
#    for td in _plainText.select('td:nth-of-type(3)'):
    for i, td in enumerate(_plainText.select('td')):
        if i == 2:
            return td.text

def _get_Lat(_plainText):
    for i, td in enumerate(_plainText.select('td')):
        if i == 4:
            return td.text[:-2]

def _get_Lng(_plainText):
    for i, td in enumerate(_plainText.select('td')):
        if i == 5:
            return td.text[:-2]

def _get_Title(_plainText):
    for i, td in enumerate(_plainText.select('td')):
        if i == 6:
            return td.text

def _get_Tag(_origin ,_plainText):
    #c = re.compile(r'(/\D+_\d+_\d{3}.png)')
    c = re.compile(r'(/\D+[a-zA-Z0-9_]+.png)')
    if not len(_plainText.select('a')) == 0:
        for tag in _plainText.select('a'):
            plain_text = str(tag['onclick'])
            src_img = c.findall(plain_text)
            return _origin + src_img[0]
    else:
        return ""
"""