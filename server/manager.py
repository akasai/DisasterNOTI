from server import db, model

class SingletonType(type):
    def __call__(_cls, *args, **kwargs):
        try:
            return _cls.__intsance
        except AttributeError:
            _cls.__instance = super(SingletonType, _cls).__call__(*args, **kwargs)
            return _cls.__instance

class APIController(metaclass=SingletonType):
    def process(self, _type, *_data):
        if _type == "home":
            return_key = str(DBC.query("getToken",*_data))
            return return_key
        elif _type == "auth":
            if str(DBC.query("setToken", *_data)) == "success":
                DBC.commit()
            

#### 아래부터 수정중 DBconnection
class DBController(metaclass=SingletonType):
    cursor = db.cursor()
    def query(self, _model, *_args):
        if _model == "getToken":
            return model.tokenSelect(self.cursor, _args[0])
        elif _model == "setToken":
            return model.tokenInsert(self.cursor, _args[0], _args[1])

    def commit(self):
        db.commit()
    '''

    def query(self, model, *args):
        if model == User:
            user_key = args[0]
            return User.query.filter_by(user_key=user_key).first()
        elif model == Menu:
            if len(args) == 3:
                date = args[0]
                place = args[1]
                time = args[2]
                return Menu.query.filter_by(date=date, place=place, time=time).first()
        elif model == Poll:
            if len(args) == 2:
                menu = args[0]
                user = args[1]
                return Poll.query.filter_by(menu=menu, user=user).first()

    def updateUserActionDate(self, user_key):
        u = self.query(User, user_key)
        if u:
            u.last_active_date = datetime.strftime(
                datetime.utcnow() + timedelta(hours=9),
                "%Y.%m.%d %H:%M:%S")
            self.commit()
        else:
            self.addUser(user_key)

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
APIC = APIController()
DBC = DBController()