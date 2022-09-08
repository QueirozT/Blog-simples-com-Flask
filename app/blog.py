from crypt import methods
from flask import Blueprint, current_app, request, jsonify, render_template

bp_blog = Blueprint('blog', __name__)


@bp_blog.route('/', methods=['GET'])
@bp_blog.route('/index.html', methods=['GET'])
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
