from flask_wtf import FlaskForm
from wtforms import (
    BooleanField, PasswordField, StringField, SubmitField, TextAreaField
)
from wtforms.validators import (
    DataRequired, Email, EqualTo, Length, ValidationError
)

from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember_me = BooleanField('Lembrar')
    submit = SubmitField('Entrar')


class RegistrationForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    password2 = PasswordField(
        'Repetir Senha', validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(
                'Por favor, use um nome de usuário diferente.'
            )

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Por favor, use um e-mail diferente.')


class EditProfileForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired()])
    about_me = TextAreaField('Sobre mim', validators=[Length(min=0, max=200)])
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
    post = TextAreaField(
        'Conte aos outros o que está pensando!', 
        validators=[DataRequired(), Length(min=1, max=200)]
    )
    submit = SubmitField('Enviar')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    submit = SubmitField('Solicitar redefinição de senha')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Senha', validators=[DataRequired()])
    password2 = PasswordField(
        'Repetir Senha', validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField('Redefinir a senha')