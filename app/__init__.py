# FLASK
from flask import Flask
from flask import Blueprint

# SQLALCHEMY
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy.ext.declarative

from flask_bootstrap import Bootstrap

# LoginManager
from flask_login import LoginManager

# Cache
from flask_caching import Cache

from flask_qrcode import QRcode

# Pathlib
import pathlib

app = Flask(__name__, template_folder='./templates')

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://ofnssxpp:rkFM7lCrY68xsNm2HOHOit83Zev0M_PA@babar.db.elephantsql.com/ofnssxpp"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = "d2c0c9bd6d9b73303905bdc560c7007576f98faf"

login_manager =  LoginManager(app)

ModelBase = sqlalchemy.ext.declarative.declarative_base()
db = SQLAlchemy(app)
cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache'})
QRcode(app)

# Blueprints
from app.routes.group.route import group_blueprint
from app.routes.user.route import user_blueprint
from app.routes.module.route import module_blueprint
from app.routes.page.route import page_blueprint
from app.routes.auth.route import auth_blueprint

app.register_blueprint(auth_blueprint)
app.register_blueprint(group_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(module_blueprint)
app.register_blueprint(page_blueprint)

login_manager.blueprint_login_views = auth_blueprint