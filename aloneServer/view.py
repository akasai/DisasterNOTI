from aloneServer import app
from aloneServer.pulse import Pulse
from aloneServer.util import tool, errLog
from aloneServer.util import ENC
from flask import request, render_template, redirect
from multiprocessing import Queue

logger = errLog.ErrorLog.__call__()

@app.route('/', methods=["GET"])
def index():
    from aloneServer.manager import APIC
    
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
                    return tool.HTTPError(412, "Wrong URL", userIP)
                else:
                    return redirect("/pulse?Key="+key+"URI="+uri)
            else:
                return tool.HTTPError(401,'Check Your Authorization Key',userIP)

@app.route('/auth', methods=['GET','POST'])
def auth():
    from aloneServer.manager import APIC
    
    userIP = request.remote_addr
    if request.method == 'POST':
        type_1 = request.form['pulse_permission']
        type_2 = request.form['noti_permission']
        encryptKey = ENC.keyEncrypt(userIP)
        
        if APIC.process("auth", userIP, encryptKey):
            logger.writeLog("info", "Token issued : {0}".format(userIP))
            return render_template("auth.html", key=encryptKey)
        else:
            return tool.HTTPError(500, 'Token issued Failed.', userIP)
    elif request.method == 'GET':
        return tool.HTTPError(403, 'Unauthorized Access!', userIP)

@app.route('/pulse', methods=['GET'])
def pulse():
    from aloneServer.manager import APIC

    key = request.args.get('Key')
    userIP = request.remote_addr
    if APIC.process("valid", key):
        uri = request.args.get('URI')
        
        if len(uri) < 10:
            return tool.HTTPError(412, "Wrong URL", userIP)
        else:
            try:
                done_queue = Queue()
                pulse_proc = Pulse(uri, done_queue, key)
                pulse_proc.start()
                resp = done_queue.get()
            except BaseException as e:
                return tool.HTTPError(500, "Wrong URL : {0}".format(e), userIP)
            finally:
                done_queue.close()
                done_queue.join_thread()
                pulse_proc.join()
                return resp
    else:
        return tool.HTTPError(401,'Check Your Authorization Key', userIP)