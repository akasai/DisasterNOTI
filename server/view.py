from server import app
from errLog import ErrCon
from tool import ENC
from .manager import APIC
from .pulse import Pulse

from flask import request, render_template, abort, redirect
from time import localtime, strftime, ctime
from multiprocessing import Process, current_process, Queue


def error(_statusCode, _msg, _ip=None):
    ErrCon.viewLog("warning", "[{0}]{1} : {2}".format(_statusCode, _msg, _ip))
    return abort(_statusCode, 'Access Denied. '+str(_msg))

@app.route('/', methods=["GET"])
def index():
    if request.method == 'GET':
        key = request.args.get('Key')
        uri = request.args.get('URI')
        userIP = request.remote_addr
        decrypt_Key = APIC.process("home", userIP)
        
        if key == None:
            if decrypt_Key =='None':
                return render_template("index.html")
            else:
                return render_template("auth.html", key=decrypt_Key)
        else:
            if key == decrypt_Key:
                if uri == None:
                    return error(412, "Wrong URL", userIP)
                else:
                    return redirect("/pulse?Key="+key+"URI="+uri)
            else:
                return error(401,'Check Your Authorization Key',userIP)

@app.route('/auth', methods=['GET','POST'])
def auth():
    userIP = request.remote_addr
    if request.method == 'POST':
        type_1 = request.form['pulse_permission']
        type_2 = request.form['noti_permission']
        encryptKey = ENC.keyEncrypt(userIP)
        
        APIC.process("auth", userIP, encryptKey)

        ErrCon.viewLog("info", "Token issued : {0}".format(userIP))
        return render_template("auth.html", key=encryptKey)
    elif request.method == 'GET':
        return error(403, 'Unauthorized Access!', userIP)

@app.route('/pulse', methods=['GET'])
def pulse():
    key = request.args.get('Key')
    userIP = request.remote_addr
    
    if APIC.process("valid", key):
        uri = request.args.get('URI')
        
        if len(uri) < 10:
            return error(412, "Wrong URL", userIP)
        #프로세스 로직이 꼬인듯?
        else:
            try:
                done_queue = Queue()
                #setRespJson(uri, done_queue)
                pulse_proc = Pulse(uri, done_queue)
                pulse_proc.start()
                #module_proc = Process(target=setRespJson(uri, done_queue), name='Pulse-Process'+strftime('%m%d%H%M%S', localtime()))
                #module_proc.start()
                print("\n\t[{0}]\n\t* PulseData Call - [{1}]\n\t[{2}]\n".format(ctime(), key, module_proc.name))
                ErrCon.viewLog("info", "PulseData Call : {0}".format(userIP))
                resp = done_queue.get()
            except BaseException as e:
                print(e)
                return error(412, "Wrong URL", userIP)
            finally:
                print("\n\t[{0}]\n\t* PulseData Success Return\n\t[{1} Close]\n".format(ctime(), module_proc.name))
                errLog.viewLog("info", "PulseData Return : {0}".format(userIP))
                done_queue.close()
                done_queue.join_thread()
                module_proc.join()
                return resp
    else:
        return error(401,'Check Your Authorization Key', userIP)