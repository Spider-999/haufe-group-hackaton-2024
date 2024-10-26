from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, SubmitField, EmailField, PasswordField, SelectField, TextAreaField
from wtforms.validators import DataRequired, EqualTo,Email, ValidationError
from flask_login import current_user
from .models import User


class RegisterForm(FlaskForm):
    first_name = StringField('Nume', validators=[DataRequired()])
    last_name = StringField('Prenume', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Parola', validators=[DataRequired()])
    password_confirm = PasswordField('Confirma parola', validators=[DataRequired(), EqualTo('password')])
    college = SelectField('Facultate', choices=[('UPT'), ('UVT'), ('UMFT')], validators=[DataRequired()])
    submit = SubmitField('Inregistrare')


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Parola', validators=[DataRequired()])
    submit = SubmitField('Autentificare')


class PartyPostForm(FlaskForm):
    title = StringField('Titlu', validators=[DataRequired()])
    content = TextAreaField('Informatii', validators=[DataRequired()])
    location = StringField('Locatie', validators=[DataRequired()])
    submit = SubmitField('Posteaza')


class PartyPostComment(FlaskForm):
    content = TextAreaField('Continut', validators=[DataRequired()])
    submit = SubmitField('Comenteaza')


class UpdateAccountForm(FlaskForm):
    username = StringField('Nume utilizator', validators=[DataRequired()])
    picture = FileField('Schimba Avatarul', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Actualizeaza')


    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Numele de utilizator este luat.')
    