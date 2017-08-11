from aloneServer import app
from aloneServer.pulse import Pulse
from aloneServer.util import tool, errLog
from aloneServer.util import ENC
from flask import request, render_template, redirect
from multiprocessing import Queue

logger = errLog.ErrorLog.__call__()
"""
    API서버 Index Page
    
    * Token Key가 이미 발급됬을 경우
    key확인 Page로 redirect

    * Token Key가 미발급됬을 경우
    key발급 절차 진행
"""
@app.route('/', methods=["GET"])
def index():
    from aloneServer import socketio
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
"""
    API서버 Auth Page

    * key발급 절차완료 후 Token Key출력

    * 외부접근 불가능
"""
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
"""
    API서버 Pulse Page

    * pulse Data 요청에 대한 return 기능 수행

    * 외부접근 가능 [PARAMETER : TOKEN KEY, TARGET URI]
"""
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
"""
    API서버 Detect Admin

    * 서버시작 후 Detect기능 활성화를 위한 ADMIN Page
"""
@app.route('/admin', methods=['GET'])
def admin():
    from aloneServer import jobs
    twit = "Ready"
    web = "Ready"
    keyword = "Ready"
    news = "Ready"

    if len(jobs) is not 0:
        if jobs['twit']:
            twit = "Twiter Detecting...."

        if jobs['web']:
            web = "Web Detecting...."

        if jobs['key']:
            keyword = "RealTime Keyword Detecting...."

        if jobs['key']:
            news = "NEWS Detecting...."

    return render_template("admin.html", twit=twit, web=web, keyword=keyword, news=news)
"""
    API서버 Twit Detect

    * 서버시작 후 Twit Detect기능 활성화 기능 수행

    * 외부접근 불가능, Root User만 활성화 가능,[PARAMETER : Key]
"""
@app.route('/twit', methods=['GET', 'POST'])
def twit():
    from aloneServer.manager import APIC
    userIP = request.remote_addr
    
    if request.method == 'POST':
        key = request.form['Key']

        if len(key) is 0:
            return tool.HTTPError(401,'Check Your Authorization Key',userIP)

        if not APIC.process("admin", key):
            return tool.HTTPError(403, 'Unauthorized Access!', key)

        from aloneServer import socketio, jobs
    
        if jobs['twit']:
            return tool.HTTPError(423, 'Already Detecting.')
        else: #첫 접근
            from aloneServer.detect import twitDetect, config
            proc = twitDetect.TwitDetect(**config.Detect_Config.twitConfig, _sock = socketio)
            jobs['twit'] = proc
            proc.start()
        
        return "Twiter Detecting...."
    elif request.method == 'GET':
        return tool.HTTPError(403,'Wrong Access', userIP)
"""
    API서버 Web Detect

    * 서버시작 후 Web Detect기능 활성화 기능 수행

    * 외부접근 불가능, Root User만 활성화 가능,[PARAMETER : Key]
"""
@app.route('/web', methods=['GET','POST'])
def web():
    from aloneServer.manager import APIC
    userIP = request.remote_addr

    if request.method == 'POST':
        key = request.form['Key']

        if len(key) is 0:
            return tool.HTTPError(401,'Check Your Authorization Key',userIP)
    
        if not APIC.process("admin", key):
            return tool.HTTPError(403, 'Unauthorized Access!', key)

        from aloneServer import socketio, jobs
    
        if jobs['web']:
            return tool.HTTPError(423, 'Already Detecting.')
        else: #첫 접근
            from aloneServer.detect import webDetect, config
            proc = webDetect.WebDetect(**config.Detect_Config.webConfig_2)
            jobs['web'] = proc
            proc.start()
    
        return "Web Detecting...."
    elif request.method == 'GET':
        return tool.HTTPError(403,'Wrong Access', userIP)
"""
    API서버 Key Detect

    * 서버시작 후 Key Detect기능 활성화 기능 수행

    * 외부접근 불가능, Root User만 활성화 가능,[PARAMETER : Key]
"""
@app.route('/realKey', methods=['GET','POST'])
def realKey():
    from aloneServer.manager import APIC
    userIP = request.remote_addr

    if request.method == 'POST':
        key = request.form['Key']

        if len(key) is 0:
            return tool.HTTPError(401,'Check Your Authorization Key',userIP)
    
        if not APIC.process("admin", key):
            return tool.HTTPError(403, 'Unauthorized Access!', key)

        from aloneServer import socketio, jobs
        
        if jobs['key']:
            return tool.HTTPError(423, 'Already Detecting.')
        else: #첫 접근
            from aloneServer.detect import keyDetect, config
            proc = keyDetect.KeyDetect(**config.Detect_Config.keyConfig)
            jobs['key'] = proc
            proc.start()
    
        return "RealTime Keyword Detecting...."
    elif request.method == 'GET':
        return tool.HTTPError(403,'Wrong Access', userIP)

"""
    API서버 News Detect

    * 서버시작 후 News Detect기능 활성화 기능 수행

    * 외부접근 불가능, Root User만 활성화 가능,[PARAMETER : Key]
"""
@app.route('/news', methods=['GET','POST'])
def news():
    from aloneServer.manager import APIC
    userIP = request.remote_addr

    if request.method == 'POST':
        key = request.form['Key']

        if len(key) is 0:
            return tool.HTTPError(401,'Check Your Authorization Key',userIP)
    
        if not APIC.process("admin", key):
            return tool.HTTPError(403, 'Unauthorized Access!', key)

        from aloneServer import socketio, jobs
        
        if jobs['news']:
            return tool.HTTPError(423, 'Already Detecting.')
        else: #첫 접근
            from aloneServer.detect import newsDetect, config
            proc = newsDetect.NewsDetect(**config.Detect_Config.newsConfig)
            jobs['news'] = proc
            proc.start()
    
        return "NEWS Detecting...."
    elif request.method == 'GET':
        return tool.HTTPError(403,'Wrong Access', userIP)