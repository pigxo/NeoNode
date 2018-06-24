

from flask import Flask
from flask_jsonrpc import JSONRPC
from flask_socketio import SocketIO, emit,join_room
from flask_sqlalchemy import SQLAlchemy
import pymysql
from flask_cors import CORS
from config import setting

pymysql.install_as_MySQLdb()

app = Flask(__name__,template_folder="../")
cors = CORS(app, support_credentials=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@%s/%s' %(setting.MYSQLDATABASE["user"],
                                                                setting.MYSQLDATABASE["passwd"],
                                                                setting.MYSQLDATABASE["host"],
                                                                setting.MYSQLDATABASE["db_account_info"])
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=True
db = SQLAlchemy(app)
jsonrpc = JSONRPC(app, "/")
socketio = SocketIO(app)




from .controller import *
