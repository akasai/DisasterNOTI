import multiprocessing
from flask import request
from multiprocessing import Process, current_process
from tool import Tool
from errLog import ErrCon

class Pulse(Process):
    def __init__(self, _uri, _q, _key):
        Process.__init__(self)
        self.uri = _uri
        self.q = _q
        self.key = _key
        self.userIP = request.remote_addr
        ErrCon.viewLog("info", "PulseData Call : {0} [{1}]".format(self.userIP, self.key))

    def run(self):
        multiprocessing.log_to_stderr()
        ErrCon.setProcessLogger(multiprocessing.get_logger(), 10)
        Tool.setRespJson(self.uri, self.q)

    def __del__(self):
        try:
            ErrCon.viewLog("info", "PulseData Success Return : {0} [{1}]".format(self.userIP, self.key))
        except:
            pass