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
