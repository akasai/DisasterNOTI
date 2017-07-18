from server import app, errLog
from Tool.CommonTool import ENC
from .manager import APIC

from flask import request, render_template, abort

def error(_statusCode, _msg, _ip=None):
    errLog.viewLog("warning", "[{0}]{1} : {2}".format(_statusCode,_msg,_ip))
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
        else:
            pass #계속
    else:
        return error(401,'Check Your Authorization Key', userIP)
    
    
    
    '''
    else:
        
        
        
        
            try:
                done_queue = Queue()
            
                module_proc = Process(target=setRespJson, args=(uri, done_queue,), name='Pulse-Process'+strftime('%m%d%H%M%S', localtime()))
                module_proc.start()

                print("\n\t[{0}]\n\t* PulseData Call - [{1}]\n\t[{2}]\n".format(ctime(), key, module_proc.name))

                resp = callback + "(" + done_queue.get() + ")"
                done_queue.close()
                return returnJson(resp, module_proc)
            except BaseException as e:
                print(e)
                return error(412, "Wrong URL")
    '''