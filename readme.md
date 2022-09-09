# BLOG SIMPLES COM FLASK

Estou iniciando este projeto para entender melhor como o flask funciona, e aplicar o conhecimento que obtive estudando as suas ferramentas.

## Ferramentas usadas?

- gunicorn - Ferramenta de WSGI
- python-decouple - Ferramenta de gestão de variáveis de ambiente
- Flask - Framework web
- Flask-WTF - Wrapper para criação de formulários
- Flask-Babel - Wrapper para manipulação de fuso e idioma
- Flask-SQLAlchemy - Ferramenta de ORM
- Flask-Migrate - Wrapper para migração de banco de dados
- Werkzeug - Ferramenta responsável por gerar e validar Hashs
- Flask-Login - Extenção para gerenciamento de autenticação
- Email-Validator - Complemento para o flask-wtf


## Como rodar?

```sh
python wsgi.py
```

ou

```sh
gunicorn wsgi:app
```

## Como migrar o banco de dados?

```sh
flask db init
flask db migrate
flask db upgrade
```

## Como acessar a instância do app e testar o banco de dados?

Primeiro, deve entrar no shell.

```sh
flask shell
```

Após acessar o shell do flask, você tem acesso a instância do app e aos models, o que te permite fazer todos os testes e acessar o banco de dados.

```sh
>>> from app.models import User, Post
>>> db = app.db
```
