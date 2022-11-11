from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    senha2 = PasswordField('Confirme a senha', validators=[DataRequired(), EqualTo('senha')])
    submit = SubmitField("Registrar-se")

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    remember = BooleanField('Lembre-me')
    entrar = SubmitField('Entrar')

class SearchForm(FlaskForm):
    periodo = StringField('periodo')
    submit = SubmitField('Enviar')