from app import app, db
from app.models.Models import User, UserGroup, Group, Module, GroupModule, Page, ModulePage, Label, Trigger, Image
from datetime import datetime

numero_usuarios = 500
numero_paginas = numero_usuarios * 2
numero_elementos = numero_paginas * 2

print(f"Iniciando em: {datetime.now()}")

with app.app_context():
    db.drop_all()
    db.create_all()

with app.app_context():
    group01 = Group(name = 'Administrador')
    group02 = Group(name = 'Financeiro')
    group03 = Group(name = 'RH')
    group04 = Group(name = 'Infraestrutura')
    group05 = Group(name = 'Usuario Padrao')

    db.session.add(group01)
    db.session.add(group02)
    db.session.add(group03)
    db.session.add(group04)
    db.session.add(group05)

    db.session.commit()

    groups = [group01, group02, group03, group04, group05]

    [db.session.refresh(i) for i in groups]

    print("Grupos criados.")

with app.app_context():
    
    users_prepare = [User(login = f'usuario_{n+1}') for n in range(numero_usuarios)]
    
    [db.session.add(i) for i in users_prepare]

    db.session.commit()

    [db.session.refresh(i) for i in users_prepare]

    print("Usuários criados.")

with app.app_context():

    user_group = []

    for i in users_prepare:
        for n in groups:
            user_group.append(UserGroup(id_group = n.id, id_user = i.id))            

    [db.session.add(i) for i in user_group]
    db.session.commit()

with app.app_context():

    module01 = Module(name = 'Adicao')
    module02 = Module(name = 'Consulta')
    module03 = Module(name = 'Edicao')

    modules = [module01, module02, module03]
    [db.session.add(i) for i in modules]

    db.session.commit()

    [db.session.refresh(i) for i in modules]   

    print("Modulos criados.")

with app.app_context():

    groups_modules = []

    for n in modules:
        for i in groups:
            groups_modules.append(GroupModule(id_group = i.id, id_module = n.id))

    [db.session.add(i) for i in groups_modules]
    db.session.commit()

with app.app_context():

    pages = []

    for i in range(numero_paginas):
        pages.append(Page(name = f'Pagina_{i+1}'))
        
    [db.session.add(i) for i in pages]

    db.session.commit()

    [db.session.refresh(i) for i in pages]

    print("Páginas criadas.")

with app.app_context():

    modules_pages = []

    for i in pages:
        for n in modules:
            modules_pages.append(ModulePage(id_page = i.id, id_module = n.id))
    
    [db.session.add(i) for i in modules_pages]

    db.session.commit()

    [db.session.refresh(i) for i in modules_pages]

with app.app_context():
    
    elementos = []

    import base64
    import datetime

    for p in pages:

        for i in range(numero_elementos):
            elementos.append(Label(name = f'label_{i+1}', description=f'<label id="{i+1}"></label>', id_page = p.id))
            elementos.append(Trigger(name = f'trigger_{i+1}', function_trigger=f'trigger_{i+1}_2023', id_page = p.id))
            elementos.append(Image(name = f'image_{i+1}', base64=f'{base64.b64encode(f"{datetime.datetime.timestamp(datetime.datetime.now())}".encode()).decode()}', id_page = p.id))

        print(f"Elementos da página {p.id} criados.")
        
    [db.session.add(i) for i in elementos]
    print("Finalizando.")
    db.session.commit()

        # [db.session.refresh(i) for i in elementos]

from datetime import datetime
print(f"Finalizado em: {datetime.now()}")