# -*- coding: utf-8 -*-
"""
    aloneServer
    ~~~~~

    API & Detect Server based on Flask.
    :copyright: (c) 2017 by akasai
"""
from aloneServer.config import *
#from aloneServer.util import Logger
import aloneServer.util.errLog as util


from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from multiprocessing import Process

__version__ = '0.1.0'


app = Flask(__name__)
app.config.from_object(DevConfig)
app.secret_key = "secret"
CORS(app)
socketio = SocketIO(app)

from aloneServer import view

class Server(Process):
    logger = util.ErrorLog()

    print("out : {0}".format(id(logger)))
    def __init__(self):
        Process.__init__(self)
        print("print : {0}".format(id(self.logger)))
    def run(self):
        socketio.run(app, host="0.0.0.0", port=209)
'''
from werkzeug.exceptions import abort
from werkzeug.utils import redirect
from jinja2 import Markup, escape

from .app import Flask, Request, Response
from .config import Config
from .helpers import url_for, flash, send_file, send_from_directory, \
     get_flashed_messages, get_template_attribute, make_response, safe_join, \
     stream_with_context
from .globals import current_app, g, request, session, _request_ctx_stack, \
     _app_ctx_stack
from .ctx import has_request_context, has_app_context, \
     after_this_request, copy_current_request_context
from .blueprints import Blueprint
from .templating import render_template, render_template_string

# the signals
from .signals import signals_available, template_rendered, request_started, \
     request_finished, got_request_exception, request_tearing_down, \
     appcontext_tearing_down, appcontext_pushed, \
     appcontext_popped, message_flashed, before_render_template

# We're not exposing the actual json module but a convenient wrapper around
# it.
from . import json

# This was the only thing that Flask used to export at one point and it had
# a more generic name.
jsonify = json.jsonify

# backwards compat, goes away in 1.0
from .sessions import SecureCookieSession as Session
json_available = True
'''
   