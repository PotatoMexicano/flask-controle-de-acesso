from flask import Blueprint, jsonify, render_template
from app import app, db
from app.models.Models import User

from datetime import datetime

user_blueprint = Blueprint('user', __name__, url_prefix='/user')

@user_blueprint.route('/all')
def list_all():
    return jsonify(User.listAll())

@user_blueprint.route('/<id>', methods=['GET','POST'])
def list_one(id:int = None):
    if not id:
        return jsonify('parameter [id] required.')
    
    if not str(id).isnumeric():
        return jsonify('parameter [id] required be Integer.')
    
    response = jsonify(User.listOne(int(id)))
    return response
