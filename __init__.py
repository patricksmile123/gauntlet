import os
from flask import Flask
from flask_login import LoginManager
from .db import db


app = Flask(__name__, static_folder='build')
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] =  b'WR#&f&+%78er0we=%799eww+#7^90-;s'
login = LoginManager(app)
login.login_view = 'login'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data', 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'data', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024
# app.config['MAX_CONTENT_LENGTH'] = 8

from thegauntlet.models import *

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Game=Game, LoginManager=LoginManager, WordleGuess=WordleGuess, )

from thegauntlet import server