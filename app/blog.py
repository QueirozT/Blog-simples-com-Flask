from datetime import datetime
from flask import (
    Blueprint, current_app, flash, jsonify, redirect, render_template, 
    request, url_for
)
from flask_login import current_user, login_required

from app.forms import (
    EditProfileForm, EmptyForm, MessageForm, PostForm, ReplyForm
)
from app.models import Notification, Post, User, Reply

bp_blog = Blueprint('blog', __name__)


@bp_blog.route('/', methods=['GET', 'POST'])
@bp_blog.route('/index', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)

    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False
    )
    
    next_url = url_for(
        'blog.index', page=posts.next_num
    ) if posts.has_next else None
    
    prev_url = url_for(
        'blog.index', page=posts.prev_num
    ) if posts.has_prev else None

    return render_template(
        'index.html',
        posts=posts.items, 
        next_url=next_url, 
        prev_url=prev_url
    )


@bp_blog.route('/destaques', methods=['GET'])
@login_required
def destaques():
    page = request.args.get('page', 1, type=int)

    posts = current_user.followed_posts().paginate(
        page, current_app.config['POSTS_PER_PAGE'], False
    )

    next_url = url_for(
        'blog.destaques', page=posts.next_num
    ) if posts.has_next else None
    
    prev_url = url_for(
        'blog.destaques', page=posts.prev_num
    ) if posts.has_prev else None

    return render_template(
        'index.html', 
        title='Destaques',
        posts=posts.items, 
        next_url=next_url, 
        prev_url=prev_url
    )


@bp_blog.route('/post_detalhes/<username>/<int:post_id>', methods=['GET', 'POST'])
def post_detalhes(username, post_id):
    form = ReplyForm()

    page = request.args.get('page', 1, type=int)

    post = User.query.filter_by(username=username).first_or_404().posts.filter_by(id=post_id).first_or_404()
    
    if post and post.replies.count() >= 1:
        replies = post.replies.order_by(Reply.timestamp.desc()).paginate(
            page, current_app.config['POSTS_PER_PAGE'], False
        )
        
        next_url = url_for(
            'blog.post_detalhes', 
            page=replies.next_num, 
            username=username, 
            post_id=post_id
        ) if replies.has_next else None
        
        prev_url = url_for(
            'blog.index', 
            page=replies.prev_num, 
            username=username, 
            post_id=post_id
        ) if replies.has_prev else None

        return render_template(
            'post_detalhes.html', 
            title='Detalhes da Postagem',
            post=post, 
            form=form,
            replies=replies.items, 
            next_url=next_url, 
            prev_url=prev_url
        )
    
    return render_template(
            'post_detalhes.html', 
            title='Detalhes da Postagem', 
            post=post, 
            form=form
        )


@bp_blog.route('/create_reply/<username>/<int:post_id>', methods=['POST'])
def create_reply(username, post_id):
    form = ReplyForm()

    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash('Faça login para enviar uma resposta.')
            return redirect(url_for('auth.login'))

        post = Post.query.filter_by(id=post_id).first_or_404()
        
        reply = Reply( 
            body=form.pagedown.data, 
            author=current_user,
            answered=post
        )
        current_app.db.session.add(reply)
        current_app.db.session.commit()
        flash('Sua resposta foi publicada!')

    return redirect(url_for(
        'blog.post_detalhes',
        username=username,
        post_id=post_id
    ))



@bp_blog.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()

    if form.validate_on_submit():
        post = Post(
            title=form.title.data, 
            body=form.pagedown.data, 
            author=current_user
        )
        current_app.db.session.add(post)
        current_app.db.session.commit()
        flash('Seu post foi publicado!')
        return redirect(url_for('blog.index'))

    return render_template(
        'create_post.html', 
        title='Nova Postagem', 
        form=form
    )


@bp_blog.route('/user/<username>', methods=['GET'])
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
        'user.html', 
        title='Perfil', 
        user=user, 
        posts=posts.items, 
        form=form,
        next_url=next_url, 
        prev_url=prev_url
    )


@bp_blog.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        current_app.db.session.commit()


@bp_blog.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username, current_user.email)
    if form.validate_on_submit():
        current_user.username = form.username.data.strip()
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        current_app.db.session.commit()
        flash('Suas alterações foram salvas!')
        return redirect(url_for('blog.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
        form.email.data =  current_user.email

    return render_template(
        'edit_profile.html', 
        title='Editar Perfil', 
        form=form
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


@bp_blog.route('/user/<username>/popup', methods=['GET'])
def user_popup(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = EmptyForm()
    return render_template('user_popup.html', user=user, form=form)


@bp_blog.route('/remover/post/<int:post_id>')
@login_required
def remover_post(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    
    if post.author == current_user:
        post.replies.delete()
        Post.query.filter_by(id=post_id).delete()
        current_app.db.session.commit()
        flash('Postagem removida com sucesso!')
    
    return redirect(url_for('blog.index'))
        

@bp_blog.route('/remover/reply/<int:reply_id>')
@login_required
def remover_reply(reply_id):
    reply = Reply.query.filter_by(id=reply_id).first_or_404()

    post = reply.answered

    if current_user == reply.author:
        Reply.query.filter_by(id=reply_id).delete()
        current_app.db.session.commit()
        flash('Resposta removida com sucesso!')

    return redirect(url_for(
        'blog.post_detalhes', 
        username=post.author.username, 
        post_id=post.id
    ))
