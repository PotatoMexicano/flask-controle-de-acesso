# FLASK
from flask import Flask
from flask import Blueprint

# SQLALCHEMY
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy.ext.declarative

# LoginManager
from flask_login import LoginManager

# Cache
from flask_caching import Cache

# Pathlib
import pathlib

app = Flask(__name__, template_folder='./templates')

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://ofnssxpp:rkFM7lCrY68xsNm2HOHOit83Zev0M_PA@babar.db.elephantsql.com/ofnssxpp"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = "d2c0c9bd6d9b73303905bdc560c7007576f98faf"

# login_manager =  LoginManager(app)
ModelBase = sqlalchemy.ext.declarative.declarative_base()
db = SQLAlchemy(app)
cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache'})

# Blueprints
from app.routes.group.route import group_blueprint
from app.routes.user.route import user_blueprint
from app.routes.module.route import module_blueprint
from app.routes.page.route import page_blueprint

app.register_blueprint(group_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(module_blueprint)
app.register_blueprint(page_blueprint)