#from aloneServer.db import connect, message, model
from aloneServer.db import message, model

#Singleton class
class SingletonType(type):
    _instance = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance:
            cls._instance[cls] = super(SingletonType , cls).__call__(*args, **kwargs)
        return cls._instance[cls]
    
#API Admin
class APIController(metaclass=SingletonType):
    def process(self, _type, *_data):
        if _type == "home":
            return_key = str(DBC.selectToken(*_data))
            return return_key
        elif _type == "auth":
            return message.CompMessage(DBC.insertToken(*_data)).getBool()
        elif _type == "valid":
            return message.CompMessage(DBC.selectValid(*_data)).getBool()
        elif _type == "notice":
            return message.CompMessage(DBC.noticeInsert(*_data)).getBool()

#### 아래부터 수정중 DBconnection
class DBController(metaclass=SingletonType):
    def selectToken(self, *_args):
        return model.tokenSelect(_args[0])
    
    def insertToken(self, *_args):
        return model.tokenInsert(_args[0], _args[1])
    
    def selectValid(self, *_args):
        return model.ValidSelect(_args[0])

    def noticeInsert(self, *_args):
        return model.NoticeInsert(_args[0], _args[1], _args[2])

APIC = APIController.__call__()
DBC = DBController.__call__()