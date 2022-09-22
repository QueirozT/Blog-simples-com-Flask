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
- Flask-Login - Extensão para gerenciamento de autenticação
- Email-Validator - Complemento para o flask-wtf
- Flask-Mail - Extensão para trabalhar com emails
- pyjwt - Biblioteca do python que gera tokens (Json Web Tokens)
- Flask-Moment - Wrapper da biblioteca moment.js para tratamento de datas

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

Para ter acesso aos recursos do banco de dados e testar, basta usar.
```sh
flask shell
```

A configuração foi predefinida no ```wsgi.py``` o que dá acesso direto as instãncias de "app", "db", "User" e "Post".
```py
>>> app
<Flask 'app'>

>>> db
<SQLAlchemy engine=sqlite:///>

>>> User
<class 'app.models.User'>

>>> Post
<class 'app.models.Post'>
```

## Como rodar um servidor de email local para receber os erros?

Para rodar, basta executar o comando a baixo que o python gera automaticamente um servidor local.

```sh
python -m smtpd -n -c DebuggingServer localhost:8025
```

As configurações para usar este serviço já estão definidas no env.exemplo, caso queira usar algum serviço dedicado, basta trocar os dados no seu arquivo de variáveis de ambiente.

## Como usar o flask-moment?

- Primeiro passo; precisa configurar o contexto do app como foi feito no ```__init__.py``` 
- Segundo passo; precisa inserir o ```{{ moment.include_moment() }}``` nos templates que precisar, para que o moments seja carregado.
- Terceiro passo; basta usar o jinja2 para invocar as datas e formatar através do ```{{ moment(data).fromNow() }}```
- Por último; pode acrescentar um ```{{ moment.locale(auto_detect=True) }}``` para detectar automaticamente o idioma do navegador.


Formatos de datas suportados:
```py
moment('2021-06-28T21:45:23Z').format('L') # "06/28/2021"
moment('2021-06-28T21:45:23Z').format('LL') # "June 28, 2021"
moment('2021-06-28T21:45:23Z').format('LLL') # "June 28, 2021 2:45 PM"
moment('2021-06-28T21:45:23Z').format('LLLL') # "Monday, June 28, 2021 2:45 PM"
moment('2021-06-28T21:45:23Z').format('dddd') # "Monday"
moment('2021-06-28T21:45:23Z').fromNow() # "7 hours ago"
moment('2021-06-28T21:45:23Z').calendar() # "Today at 2:45 PM"
```

## Como rodar este projeto usando o docker?

Para começar, o docker precisa estar instalado.

Como este projeto é extremamente simples, montei um esquema de imagem equivalente. tudo que precisa para funcionar é executar os comandos a seguir:

1 - Para criar a imagem a partir dos arquivos fornecidos, basta rodar o comando:
```sh
docker build -t blog-simples:latest .
```

2 - Após criar a imagem, use o comando a baixo para rodar o projeto:
- Após rodar o projeto, pode acessa-lo através do endereço: http://localhost:8000

```sh
docker run -d --rm --name blog-simples -p 8000:8000 -v $PWD:/home/blog-simples/ blog-simples:latest
```

3 - Para ver os logs do servidor, basta usar o comando a baixo ou trocar a flag "-d" por "-it" do segundo comando:
```sh
docker logs blog-simples
```

4 - Para finalizar a execução, basta usar o comando:
```sh
docker stop blog-simples
```

- Se quiser instalar algum pacote diferente, basta acrescentar ao requirements.txt e rodar o primeiro comando novamente.


Para testar os serviços de email, basta executar este comando enquanto o docker estiver ativo:
```sh
docker exec -it blog-simples python -m smtpd -n -c DebuggingServer localhost:8025
```
