from app import app, db
from app.models.Models import Group, Image, Label, Module, Page, User, Trigger
from app.models.Models import UserGroup

with app.app_context():
    db.drop_all()
    db.create_all()