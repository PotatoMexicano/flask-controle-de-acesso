# Flask-Controle-de-acesso
Projeto simples em Python (Flask) para implementar um ACL para usuários com vários níveis de objetos.

O intuito deste projeto é comparar a velocidade de processamento e carregamento dos dados implementandos as funções em **SQL bruto** comparado com implementações em **ORM**.

Além dos modelos preparados em **SQLAlchemy**, possui rotas agrupadas em **blueprints** e arquivos de **migrations** para popular o banco de dados com registros de teste.

 - [x] Controle de login / logout.
 - [x] Carregamento opcional da cadeia de elementos.
 - [x] Agrupamento das rotas em Blueprints.
 - [ ] Implementação de telas visuais para o sistema [TailwindCSS + Flowbite]

Não carregamento da cadeia de elementos: 
```json
  {
    "grupos": null,
    "id": 1,
    "login": "usuario_1"
  }
```
Carregamento da cadeia de elementos:

```json
{
    "grupos": [
      {
        "id": 1,
        "modules": null,
        "name": "Administrador"
      },
      {
        "id": 2,
        "modules": null,
        "name": "Financeiro"
      }
    ],
    "id": 1,
    "login": "usuario_1"
  }
```

*Este projeto é livre para utilização e consulta.*
