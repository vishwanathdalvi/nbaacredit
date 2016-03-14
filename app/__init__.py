from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask_wtf.csrf import CsrfProtect
from config import basedir

app = Flask(__name__)
app.config.from_object('config')
CsrfProtect(app)
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

from app import views, models
