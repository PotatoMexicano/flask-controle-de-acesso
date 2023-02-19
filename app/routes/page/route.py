from flask import Blueprint, jsonify
from app import app, db
from app.models.Models import Page

page_blueprint = Blueprint('page', __name__, url_prefix='/page')

@page_blueprint.route('/all')
@page_blueprint.route('/all/<id>')
def list_all(id:int = None):

    if id:
        return jsonify(Page.listAllowed(id))

    return jsonify(Page.listAll())

@page_blueprint.route('/<id>')
def list_one(id:int = None):
    
    if not id: 
        return jsonify('parameter [id] required.')
    
    if not id.isnumeric():
        return jsonify('parameter [id] required be Integer.')

    return jsonify(Page.listOne(id))

