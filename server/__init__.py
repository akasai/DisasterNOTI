from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

from server import view, errLog
errLog.setLogger(app,10)