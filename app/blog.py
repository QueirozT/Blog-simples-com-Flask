from flask import (
    Blueprint, current_app, flash, jsonify, redirect, render_template, request, url_for
)

from app.forms import LoginForm


bp_blog = Blueprint('blog', __name__)


@bp_blog.route('/', methods=['GET'])
@bp_blog.route('/index', methods=['GET'])
def index():
    user = {'username': 'Tiago'}
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

    return render_template(
        'index.html', 
        title='Página Inicial', 
        user=user,
        posts=posts
    )


@bp_blog.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(
            f'Um login foi solicitado para {form.username.data}, \
                lembrar={form.remember_me.data}'
        )
        return redirect(url_for('blog.index'))
    
    return render_template(
        'login.html', 
        title='Entrar', 
        form=form
    )
