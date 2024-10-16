from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from aplication.models import User
import re
from aplication import bcrypt


class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Este e-mail já está cadastrado. Por favor, use um e-mail diferente.')

    def validate_password(self, password):
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&.])[A-Za-z\d@$!%*?&.]{8,}$"
        if not re.match(pattern, password.data):
            raise ValidationError('A senha deve ter no mínimo 8 caracteres, com letra maiúscula, letra minúscula, número e caractere especial.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Manter-me logado')
    submit = SubmitField('Login')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError('Este e-mail não está cadastrado.')

    def validate_password(self, password):
        user = User.query.filter_by(email=self.email.data).first()
        if user and not bcrypt.check_password_hash(user.password, password.data):
            raise ValidationError('Senha incorreta. Tente novamente.')


class VerificationForm(FlaskForm):
    verification_code = StringField('Código de Verificação', validators=[DataRequired(), Length(min=6, max=6)])
    submit = SubmitField('Verificar E-mail')
