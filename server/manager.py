from dbConnect import db, model, message

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
            if message.CompMessage(DBC.insertToken(*_data)).getBool():
                DBC.commit()
        elif _type == "valid":
            return message.CompMessage(DBC.selectValid(*_data)).getBool()

#### 아래부터 수정중 DBconnection
class DBController(metaclass=SingletonType):
    cursor = db.cursor()
    
    def selectToken(self, *_args):
        return model.tokenSelect(self.cursor, _args[0])
    
    def insertToken(self, *_args):
        return model.tokenInsert(self.cursor, _args[0], _args[1])
    
    def selectValid(self, *_args):
        return model.ValidSelect(self.cursor, _args[0])

    def commit(self):
        db.commit()
    
'''
    def addUser(self, user_key):
        u = self.query(User, user_key)
        if u is None:
            self.add(u)
            u = User(user_key)

    def deleteUser(self, user_key):
        u = self.query(User, user_key)
        if u is not None:
            self.delete(u)

    def addPoll(self, score, menu, user):
        p = Poll(score, menu=menu, user=user)
        self.add(p)

    def addMenu(self, date, place, time, menu):
        m = Menu(date, place, time, menu)
        self.add(m)

    def delete(self, obj):
        db.session.delete(obj)
        self.commit()

    def add(self, obj):
        db.session.add(obj)
        self.commit()

    def commit(self):
        db.session.commit()

'''
APIC = APIController.__call__()
DBC = DBController.__call__()

prrin(APIC)