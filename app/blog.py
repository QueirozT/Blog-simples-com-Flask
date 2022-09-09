from flask import (
    Blueprint, current_app, flash, jsonify, redirect, render_template, 
    request, url_for
)
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse

from app.forms import LoginForm
from app.models import User


bp_blog = Blueprint('blog', __name__)


@bp_blog.route('/', methods=['GET'])
@bp_blog.route('/index', methods=['GET'])
@login_required
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Este é um belo dia!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'O novo filme dos vingadores é muito bom!'
        }
    ]

    return render_template('index.html', title='Página Inicial', posts=posts)


@bp_blog.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('blog.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Usuário ou senha inválidos')
            return redirect(url_for('blog.login'))
        
        login_user(user, remember=form.remember_me.data)
        
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('blog.index')

        return redirect(next_page)
    
    return render_template('login.html', title='Entrar', form=form)


@bp_blog.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('blog.index'))
