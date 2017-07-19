import json

from time import strftime, strptime, ctime, time
from tweepy.streaming import StreamListener

class Listener(StreamListener):
    def __init__(self, _title, _process, _format, _keywordDic, _sock):
        self.title = _title
        self.curProcess = _process
        self.format = _format
        self.tmp_time = time()
        self.sockio = _sock 

        self.keywordDic = _keywordDic
        self.counting = self.setInitial(self.keywordDic)

    def on_connect(self):
        print("[{0}]{1} \t- Detecting Start ".format(ctime(),self.title))
    
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
                        self.setCounting(i)

                if self.isOneMin(self.tmp_time):
                    for k in self.counting:
                        print("[{0}] {1}-{2}({3})\t{4}".format(ctime(), self.curProcess, self.title, k, self.checkCount(self.counting.get(k), k)))
                    self.tmp_time = time()
                    self.resetCount()

    def keep_alive(self):
        try:
            pass
        except ConnectionAbortedError as c:
            print("[{0}]{1} \t- Detecting Stoped \t{2}".format(ctime(), self.title, c))

    def on_error(self, _status):
        print(_status)
###############################################################
    def checkCount(self, _count, _key):
        db = MySQLdb.connect(host=dbServer ,port=port,user="root",passwd="1111",db="test", charset='utf8')
        cursor = db.cursor()
        percentage = (_count / 10) * 100
        try:
            if percentage > 0:#수치조정 필요
                content = "발생 추정"
                query = "insert into tb_notice(time, value, route, content, percentage) values (sysdate(), '"+_key+"', 'Twiiter', '"+content+"', "+str(int(percentage))+");"
                cursor.execute(query)
                self.sockio.emit("notification", {"message":content,"type":_key,"time":strftime("%Y/%m/%d %a %H:%M:%S", strptime(ctime(self.tmp_time)))}, broadcast=True)
            elif percentage == 0:
                content = "안전 상태"
            else:
                content = "발생 가능성 ["+str(percentage)+"%]"
        except Exception as e:
            print(e)
        finally:
            db.commit()
            db.close()
            return content
    
    def isOneMin(self, _time):
        return time() - _time > 20

    def setInitial(self, _dic):
        result = dict()
        for i, key in enumerate(_dic.keys()):
            result[key] = 0
        return result

    def setCounting(self, _index):
        for i,key in enumerate(self.counting.keys()):
            if i == _index:
                tmp = self.counting.get(key)
                self.counting[key] = int(tmp) + 1
    
    def resetCount(self):
        for i,key in enumerate(self.counting.keys()):
            self.counting[key] = 0