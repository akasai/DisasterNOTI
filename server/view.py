from server import app, errLog
from flask import request, render_template

def error(_statusCode, _msg):
    return abort(_statusCode, 'Access Denied. '+str(_msg))

@app.route('/', methods=["GET"])
def index():
    if request.method == 'GET':
        key = request.args.get('Key')
        uri = request.args.get('URI')
        #if key == None:
            #if rows == None:
        
        return render_template("index.html")
            #else:
                #return render_template("auth.html", key = rows[1].decode())

    '''
    @app.route('/')
    def index():
        if request.method == 'GET':
        
            db = MySQLdb.connect(host=dbServer,port=port,user="root",passwd="1111",db="test", charset='utf8')
            cursor = db.cursor()
            userIP = request.remote_addr
            query = "select ip, AES_DECRYPT(UNHEX(accessKey), 'acorn') from tb_access_auth where ip = '"+userIP+"';"
            cursor.execute(query)
            
            rows = cursor.fetchone()

            db.close()

            if key == None:
                if rows == None:
                    return render_template("index.html")
                else:
                    return render_template("auth.html", key = rows[1].decode())
            else:
                if key == rows[1].decode():
                    if uri == None:
                        return error(412, "Wrong URL")
                    else:
                        return redirect("/pulse?Key="+key+"URI="+uri)
                else:
                    return error(401,'Check Your Authorization Key')
    '''
    '''
@app.route('/auth', methods=['GET','POST'])
def auth():
    if request.method == 'POST':
        userIP = request.remote_addr
        type = request.form['earthquake_pulse']
        encrypt = keyEncrypt(userIP, type)

        #db = MySQLdb.connect(host=dbServer,port=port,user="root",passwd="1111",db="test", charset='utf8')
        #cursor = db.cursor()
        #query = "insert into tb_access_auth values ('"+userIP+"',HEX(AES_ENCRYPT('"+encrypt+"','acorn')),sysdate(),'"+type+"');"
        #cursor.execute(query)
        
        #db.commit()
        #db.close()
        
        return render_template("auth.html", key = encrypt)
    elif request.method == 'GET':
        return error(403, 'Unauthorized Access!')
    '''