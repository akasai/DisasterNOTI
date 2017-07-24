from multiprocessing import Process
from tool import Tool

class Pulse(Process):
    def __init__(self, _uri, _q):
        Process.__init__(self)
        self.uri = _uri
        self.q = _q

    def run(self):
        Tool.setRespJson(self.uri, self.q)
        pass

    