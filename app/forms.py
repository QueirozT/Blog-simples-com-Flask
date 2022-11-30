from flask_wtf import FlaskForm
from flask_pagedown.fields import PageDownField
from wtforms import (
    StringField, SubmitField, TextAreaField
)
from wtforms.validators import (
    DataRequired, Length, ValidationError, Email
)

from app.models import User


class EditProfileForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    about_me = PageDownField('Sobre mim')
    submit = SubmitField('Salvar')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(
                    'Por favor, use um nome de usuário diferente.'
                )


class EmptyForm(FlaskForm):
    submit = SubmitField('Enviar')


class PostForm(FlaskForm):
    title = StringField('Informe o título da publicação', validators=[DataRequired()])
    pagedown = PageDownField(validators=[DataRequired()])
    submit = SubmitField('Publicar')


class ReplyForm(FlaskForm):
    pagedown = PageDownField(validators=[DataRequired()])
    submit = SubmitField('Responder')


class MessageForm(FlaskForm):
    message = TextAreaField(
        'Mensagem', 
        validators=[DataRequired(), Length(min=1, max=140)]
    )
    submit = SubmitField('Enviar')
