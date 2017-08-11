from time import time, strptime, strftime, ctime

def checktwitCount(_sock, _count, _key, _tmptime):
    from aloneServer.manager import APIC
    percentage = (_count / 10) * 100
    try:
        if percentage > 0:#수치조정 필요
            content = "발생 추정 : {0}".format(_count)
            APIC.process("notice", _key, "twitter", content, str(int(percentage)))
            _sock.emit("notification", {"message":content,"type":_key,"time":strftime("%Y/%m/%d %a %H:%M:%S", strptime(ctime(_tmptime)))}, broadcast=True)
        elif percentage == 0:
            content = "안전 상태 : {0}".format(_count)
        else:
            content = "발생 가능성 ["+str(percentage)+"%] : {0}".format(_count)
    except Exception as e:
        print(e)
    else:
        return content
    
def isOneMin(_time):
    return time() - _time > 20

def setInitial(_dic):
    result = dict()
    for i, key in enumerate(_dic.keys()):
        result[key] = 0
    return result

def setCounting(_counting , _index):
    for i,key in enumerate(_counting.keys()):
        if i == _index:
            tmp = _counting.get(key)
            _counting[key] = int(tmp) + 1
    
def resetCount(_counting):
    for i,key in enumerate(_counting.keys()):
        _counting[key] = 0

def _get_article_Time(_itemTag, _config, _format):
    format = '%Y.%m.%d %H:%M:%S'
    tdSelect = _itemTag.select(_config['className'])
    for td in tdSelect:
        if _config['attr']:
            try:
                time_String = td.get(_config['attr']) if td.get(_config['attr']) != None else '0'
                return strftime(_format, strptime(time_String, format)) if time_String != '0' else False
            except BaseException as e:
                pass
        else:
            try:
                time_String = td.text.strip()
                return strftime(_format, strptime(time_String, _format))
            except BaseException as e:
                pass
            
def checkCount(_count, _route, _key):
    from aloneServer.manager import APIC
    percentage = (_count / 10) * 100
    try:
        if percentage > 20:#수치조정 필요
            content = "발생 추정"
            APIC.process("notice", _key, "Web", content, str(int(percentage)))
            #_sock.emit("notification", {"message":content,"type":_key,"time":strftime("%Y/%m/%d %a %H:%M:%S", strptime(ctime(self.tmp_time)))}, broadcast=True)
        elif percentage == 0:
            content = "안전 상태"
        else:
            content = "발생 가능성 ["+str(percentage)+"%]"
    except Exception as e:
        print(e)
    else:
        return content

def checkKeyword(_config, _keylist):
    for value in _config:
        for k in value:
            if k in _keylist:
                print(k) 
            else:
                print("None")


def isOccur(_ori, _cur):
    gap = _ori - _cur

    if gap > 10:
        checkCount(gap, "", "뉴스")
