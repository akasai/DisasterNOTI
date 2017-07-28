class BaseConfig(object):
    DEBUG=False
    TESTING=False

class DevConfig(BaseConfig):
    DEBUG=True
    TESTING=True

class TestConfig(BaseConfig):
    DEBUG=False
    TESTING=True

class Detect_Config:
    webConfig_1 = {
        '_title':'지진희갤러리',
        '_url':'http://gall.dcinside.com/board/lists/?id=jijinhee&page=1',
        '_format':'%Y.%m.%d %H:%M',
        '_config':{
                'rowName':'tr.tb',
                'className':'td.t_date',
                'attr':'title'
        }
    }

    webConfig_2 = {
        '_title':'루리웹',
        '_url':'http://bbs.ruliweb.com/community/board/300143/list?page=1',
        '_format':'%H:%M',
        '_config':{
                'rowName':'tr.table_body',
                'className':'td.time',
                'attr':False
        }
    }

    twitConfig = {
        '_title':'트위터',
        '_url': None,
        '_format':"%a %b %d %H:%M:%S +0000 %Y",
        '_config':{
                'rowName':'tr.table_body',
                'className':'td.time',
                'attr':False
        }
    }