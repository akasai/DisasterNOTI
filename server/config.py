class BaseConfig(object):
    DEBUG=False
    TESTING=False

class DevConfig(BaseConfig):
    DEBUG=True
    TESTING=True

class TestConfig(BaseConfig):
    DEBUG=False
    TESTING=True

class DB_Config:
    db_config = {
        'host':'192.168.0.85',
        'port':3306,
        'user':'root',
        'passwd':'1111',
        'db':'test',
        'charset':'utf8'
    }