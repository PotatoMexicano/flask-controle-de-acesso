from flask import Blueprint, jsonify
from app import app, db
from app.models.Models import Group

group_blueprint = Blueprint('group', __name__, url_prefix='/group')

@group_blueprint.route('/all')
@group_blueprint.route('/all/<id>')
def list_all(id:int = None):

    if id:
        return jsonify(Group.listAllowed(id))

    return jsonify(Group.listAll())

@group_blueprint.route('/<id>')
def list_one(id:int = None):
    
    if not id: 
        return jsonify('parameter [id] required.')
    
    if not id.isnumeric():
        return jsonify('parameter [id] required be Integer.')

    return jsonify(Group.listOne(id))

