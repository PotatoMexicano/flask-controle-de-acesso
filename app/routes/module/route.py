from flask import Blueprint, jsonify
from app import app, db
from app.models.Models import Module

module_blueprint = Blueprint('module', __name__, url_prefix='/module')

@module_blueprint.route('/all')
@module_blueprint.route('/all/<id>')
def list_all(id:int = None):

    if id:
        return jsonify(Module.listAllowed(id))

    return jsonify(Module.listAll())

@module_blueprint.route('/<id>')
def list_one(id:int = None):
    
    if not id: 
        return jsonify('parameter [id] required.')
    
    if not id.isnumeric():
        return jsonify('parameter [id] required be Integer.')

    return jsonify(Module.listOne(id))

