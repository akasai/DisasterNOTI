class Keyward:
    keywordDic = {
        "지진":{
            "지진",
            "여진",
            "진도"
        },
        "날씨이상":{
            '비',
            '폭우'
        },
        "사고":{
            "교통사고",
            "교통 사고",
            "차량사고",
            "차량 사고"
        }
    }
class Key_Config:
    consumerKey = '[own_key]'
    consumerSecret = '[own_key]'
    accessToken = '[own_key]'
    accessTokenSecret = '[own_key]'
    
class Detect_Config:
    webConfig_1 = {
        '_title':'지진희갤러리',
        '_url':'http://gall.dcinside.com/board/lists/?id=jijinhee&page=1',
        '_format':'%Y.%m.%d %H:%M',
        '_config':{
                'rowName':'tr.td ',
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
