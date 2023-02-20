from dataclasses import dataclass
from flask_login import UserMixin

from datetime import datetime

from sqlalchemy.sql import text
import sqlalchemy.orm as orm
from sqlalchemy import Column, String, Integer, DateTime, select, ForeignKey

from app import app, db

@dataclass
class Image(db.Model):

    __tablename__ = 'images'

    id:int = Column(Integer, primary_key=True, autoincrement=True)
    name:str = Column(String(45), nullable=False)
    base64:str = Column(String(), nullable=True)
    on_create = Column(DateTime, nullable=False, default=datetime.now)

    id_page = Column(Integer, ForeignKey('pages.id'), nullable=False)

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.base64 = kwargs.get('base64')
        self.id_page = kwargs.get('id_page')
    
    def listAll():
        raw = select(Image)
        response = db.session.execute(raw).all()
        return [i[0] for i in response]
    
    def listAllowed(id:int = None):
        raw = select(Image).where(Image.id_page == id)
        response = db.session.execute(raw).all()
        return [i[0] for i in response]

@dataclass
class Trigger(db.Model):

    __tablename__ = 'triggers'

    id:int = Column(Integer, primary_key=True, autoincrement=True)
    name:str = Column(String(45), nullable=False)
    function_trigger:str = Column(String(45), nullable=False)
    on_create = Column(DateTime, nullable=False, default=datetime.now)

    id_page = Column(Integer, ForeignKey('pages.id'), nullable=False)

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.function_trigger = kwargs.get('function_trigger')
        self.id_page = kwargs.get('id_page')
    
    def listAll():
        raw = select(Trigger)
        response = db.session.execute(raw).all()
        return [i[0] for i in response]
    
    def listAllowed(id:int = None):
        if not id:
            return 'parameter [id] required.'
        
        if not str(id).isnumeric():
            return 'parameter [id] required be Integer.'
        
        raw = select(Trigger).where(Trigger.id_page == id)
        response = db.session.execute(raw).all()
        return [i[0] for i in response]

@dataclass
class Label(db.Model):

    __tablename__ = 'labels'

    id:int = Column(Integer, primary_key=True, autoincrement=True)
    name:str = Column(String(45), nullable=False)
    description:str = Column(String(255), nullable=False)
    on_create = Column(DateTime, nullable=False, default=datetime.now)
    id_page = Column(Integer, ForeignKey('pages.id'), nullable=False)

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.description = kwargs.get('description')
        self.id_page = kwargs.get('id_page')
    
    def listAll():
        raw = select(Label)
        response = db.session.execute(raw).all()
        return [i[0] for i in response]    
    
    def listAllowed(id:int = None):
        if not id:
            return 'parameter [id] required.'
        
        if not str(id).isnumeric():
            return 'parameter [id] required be Integer.'
        
        raw = select(Label).where(Label.id_page == id)
        response = db.session.execute(raw).all()
        return [i[0] for i in response]

@dataclass
class Page(db.Model):

    __tablename__ = 'pages'
    __allow_unmapped__ = True

    id:int = Column(Integer, primary_key=True, autoincrement=True)
    name:str = Column(String(45), nullable=False)
    on_create =  Column(DateTime, nullable=False, default=datetime.now)

    images = None
    triggers = None
    labels = None

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
    
    @orm.reconstructor
    def loadRelationship(self):
        self.images = Image.listAllowed(self.id)
        self.triggers = Trigger.listAllowed(self.id)
        self.labels = Label.listAllowed(self.id)

    def listAll():
        raw = select(Page)
        response = db.session.execute(raw).all()
        return [i[0] for i in response]

    def listOne(id:int = None):
        if not id:
            return 'parameter [id] required.'
        
        if not str(id).isnumeric():
            return 'parameter [id] required be Integer.'
        
        raw = select(Page).where(Page.id == id)
        response = db.session.execute(raw).first()
        return [i for i in response]

    def listAllowed(id:int = None):
        if not id:
            return 'parameter [id] required.'
        
        raw = select(Page)\
            .join(ModulePage, Page.id == ModulePage.id_page)\
            .where(ModulePage.id_module == id)
        response = db.session.execute(raw).all()

        if len(response) >= 1:
            return [i[0] for i in response]
        
        return None

@dataclass
class ModulePage(db.Model):
    __tablename__ = 'modules_pages'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_page = Column(Integer, ForeignKey('pages.id'), nullable=False)
    id_module = Column(Integer, ForeignKey('modules.id'), nullable=False)
    on_create = Column(DateTime, nullable=False, default=datetime.now)

    def __init__(self, **kwargs) -> None:
        self.id_page = kwargs.get('id_page')
        self.id_module = kwargs.get('id_module')

@dataclass
class Module(db.Model):

    __tablename__ = 'modules'
    __allow_unmapped__ = True

    id:int = Column(Integer, primary_key=True, autoincrement=True)
    name:str = Column(String(45), nullable=False)
    on_create = Column(DateTime, nullable=False, default=datetime.now)

    pages = None

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')

    def listAll():
        raw = select(Module)
        response = db.session.execute(raw).all()
        return [i[0] for i in response]
    
    def listOne(id:int = None):
        if not id:
            return 'parameter [id] required.'
        
        if not str(id).isnumeric():
            return 'parameter [id] required be Integer.'
        
        raw = select(Module).where(Module.id == id)
        response = db.session.execute(raw).first()
        return [i for i in response]

    def listAllowed(id:int = None):
        if not id:
            return 'parameter [id] required.'
        
        raw = select(Module)\
            .join(GroupModule, Module.id == GroupModule.id_module)\
            .where(GroupModule.id_group == id)
        response = db.session.execute(raw).all()

        if len(response) >= 1:
            return [i[0] for i in response]
        
        return None

@dataclass
class Group(db.Model):
    __tablename__ = 'groups'
    __allow_unmapped__ = True
    
    id:int = Column(Integer, primary_key=True, autoincrement=True)
    name:str = Column(String(45), nullable=False)
    on_create = Column(DateTime, default=datetime.now, nullable=False)

    modules = None

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.on_create = kwargs.get('on_create', datetime.now())

    def listAll():
        raw = select(Group)
        response = db.session.execute(raw).all()
        return [i[0] for i in response]
    
    def listOne(id:int = None):
        if not id:
            return 'parameter [id] required.'
        
        if not str(id).isnumeric():
            return 'parameter [id] required be Integer.'

        raw = select(Group).where(Group.id == id)
        response = db.session.execute(raw).first()

        if not response:
            return 'object not found.'
            
        return [i for i in response]

    def listAllowed(id:int = None):
        if not id:
            return 'parameter [id] required.'
        
        raw = select(Group)\
            .join(UserGroup, Group.id == UserGroup.id_group)\
            .where(UserGroup.id_user == id)
        response = db.session.execute(raw).all()

        if len(response) >= 1:
            return [i[0] for i in response]
        
        
        return None
            
@dataclass
class UserGroup(db.Model):
    __tablename__ = 'users_group'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_user = Column(Integer, ForeignKey('users.id'), nullable=False)
    id_group = Column(Integer, ForeignKey('groups.id'), nullable=False)
    on_create = Column(DateTime, nullable=False, default=datetime.now)

    def __init__(self, **kwargs) -> None:
        self.id_group = kwargs.get('id_group')
        self.id_user = kwargs.get('id_user')
    
    def __str__(self) -> str:
        return f"<UserGroup: user='{self.id_user}' group='{self.id_group}'>"

@dataclass
class User(db.Model, UserMixin):
    
    __tablename__ = 'users'
    __allow_unmapped__ = True

    id:int = Column(Integer, primary_key=True, autoincrement=True)
    login:str = Column(String(45), nullable=False, unique=True)
    password = Column(String(100), nullable=False, default='default password')
    on_create = Column(DateTime, nullable=False, default=datetime.now)
    on_login = Column(DateTime, nullable=True)

    grupos = None
    
    def __init__(self, **kwargs):
        self.login = kwargs.get('login')

    def loadRelationship(self, grupo:bool = False, modulo:bool = False, pagina:bool = False):

        if pagina:
            grupo = True
            modulo = True

        if modulo:
            grupo = True

        if grupo:
            self.grupos = Group.listAllowed(self.id)
        
        if modulo and grupo:
            for group in self.grupos:
                group.modules = Module.listAllowed(group.id)

                if pagina and modulo and grupo:
                    for module in group.modules:
                        module.pages = Page.listAllowed(module.id)
            
    def listAll():
        raw = select(User)
        response = db.session.execute(raw).all()
        response = [i[0] for i in response]
        return response
    
    def listOne(id:int = None):

        if not id:
            return 'parameter [id] required.'
    
        if not str(id).isnumeric():
            return 'parameter [id] required be Integer.'
        
        raw = select(User).where(User.id == id)
        response = db.session.execute(raw).first()

        if not response:
            return 'object not found.'

        response:User = response[0]
        response.loadRelationship(grupo=True)
        
        return [response]

    def hasAdminRole(self):

        if len([i for i in self[0].grupos if i.id == 1]) >= 1:
            return True

        return False

@dataclass
class GroupModule(db.Model):
    __tablename__ = 'groups_modules'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_group = Column(Integer, ForeignKey('groups.id'), nullable=False)
    id_module = Column(Integer, ForeignKey('modules.id'), nullable=False)
    on_create = Column(DateTime, nullable=False, default=datetime.now)

    def __init__(self, **kwargs) -> None:
        self.id_group = kwargs.get('id_group')
        self.id_module = kwargs.get('id_module')
