from datetime import datetime
from flask import (
    Blueprint, current_app, flash, redirect, render_template, 
    request, url_for
)
from flask_login import current_user, login_required

from app.forms import (
    EditProfileForm, EmptyForm, PostForm
)
from app.models import User, Post

bp_blog = Blueprint('blog', __name__)


@bp_blog.route('/', methods=['GET', 'POST'])
@bp_blog.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        current_app.db.session.add(post)
        current_app.db.session.commit()
        flash('Seu post foi publicado!')
        return redirect(url_for('blog.index'))
    
    page = request.args.get('page', 1, type=int)

    posts = current_user.followed_posts().paginate(
        page, current_app.config['POSTS_PER_PAGE'], False
    )

    next_url = url_for(
        'blog.index', page=posts.next_num
    ) if posts.has_next else None
    
    prev_url = url_for(
        'blog.index', page=posts.prev_num
    ) if posts.has_prev else None

    return render_template(
        'index.html', title='Página Inicial', form=form, 
        posts=posts.items, next_url=next_url, prev_url=prev_url
    )


@bp_blog.route('/user/<username>', methods=['GET'])
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    
    page = request.args.get('page', 1, type=int)

    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False
    )

    next_url = url_for(
        'blog.user', username=user.username, page=posts.next_num
    ) if posts.has_next else None
    
    prev_url = url_for(
        'blog.user', username=user.username, page=posts.prev_num
    ) if posts.has_prev else None

    form = EmptyForm()

    return render_template(
        'user.html', user=user, posts=posts.items, form=form,
        next_url=next_url, prev_url=prev_url
    )


@bp_blog.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        current_app.db.session.commit()


@bp_blog.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data.strip()
        current_user.about_me = form.about_me.data
        current_app.db.session.commit()
        flash('Suas alterações foram salvas!')
        return redirect(url_for('blog.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me

    return render_template(
        'edit_profile.html', title='Editar Perfil', form=form
    )



@bp_blog.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash(f'Usuário {username} não encontrado')
            return redirect(url_for('blog.index'))
        if user == current_user:
            flash('Você não pode seguir a sim mesmo.')
            return redirect(url_for('blog.index'))
        current_user.follow(user)
        current_app.db.session.commit()
        flash(f'Você está seguindo {username}!')
        return redirect(url_for('blog.user', username=username))
    else:
        return redirect(url_for('blog.index'))


@bp_blog.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('Usuário {username} não encontrado')
            return redirect(url_for('blog.index'))
        if user == current_user:
            flash('Você não pode parar de seguir a sim mesmo.')
            return redirect(url_for('blog.user', username=username))
        current_user.unfollow(user)
        current_app.db.session.commit()
        flash(f'Você não está mais seguindo {username}')
        return redirect(url_for('blog.user', username=username))
    else:
        return redirect(url_for('blog.index'))


@bp_blog.route('/explore', methods=['GET'])
@login_required
def explore():
    page = request.args.get('page', 1, type=int)

    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False
    )
    
    next_url = url_for(
        'blog.explore', page=posts.next_num
    ) if posts.has_next else None
    
    prev_url = url_for(
        'blog.explore', page=posts.prev_num
    ) if posts.has_prev else None

    return render_template(
        'index.html', title='Explorar', posts=posts.items, 
        next_url=next_url, prev_url=prev_url
    )


@bp_blog.route('/user/<username>/popup', methods=['GET'])
@login_required
def user_popup(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = EmptyForm()
    return render_template('user_popup.html', user=user, form=form)
