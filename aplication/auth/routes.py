from flask import Blueprint, render_template, redirect, url_for, flash, request
from aplication.auth.forms import LoginForm, RegistrationForm, VerificationForm
from aplication.models import User
from aplication import bcrypt, db, mail
from flask_login import login_user, logout_user, current_user, login_required
from flask_mail import Message
import secrets
from datetime import timedelta

auth = Blueprint('auth', __name__)


# Função para enviar o código de verificação por e-mail
def send_verification_email(email, verification_code):
    msg = Message('Verificação de E-mail - MeuClima', recipients=[email])

    # Corpo do e-mail em HTML
    msg.html = f"""
    <html>
    <head>
        <style>
            .container {{
                font-family: Arial, sans-serif;
                max-width: 600px;
                margin: auto;
                padding: 20px;
                border: 1px solid #ddd;
                border-radius: 10px;
                background-color: #f9f9f9;
            }}
            .header {{
                text-align: center;
                padding: 10px;
            }}
            .header img {{
                width: 150px;
            }}
            .code {{
                font-size: 2em;
                font-weight: bold;
                color: #333;
            }}
            .content {{
                font-size: 16px;
                margin-top: 20px;
            }}
            .footer {{
                font-size: 14px;
                color: #555;
                text-align: center;
                margin-top: 30px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="content">
                <p>Olá!</p>
                <p>Seu código de verificação é:</p>
                <p class="code">{verification_code}</p>
                <p>Por favor, insira esse código no site para confirmar sua identidade.</p>
            </div>
            <div class="footer">
                <p>Se você não solicitou esse código, por favor, ignore este e-mail.</p>
            </div>
        </div>
    </body>
    </html>
    """
    # Enviando o e-mail
    mail.send(msg)


@auth.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:  # Se o usuário já estiver logado, redireciona para o dashboard
        flash('Você já está logado.', 'info')
        return redirect(url_for('main.dashboard'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        verification_code = secrets.token_hex(3)  # Gera um código aleatório de 6 caracteres

        # Criação do novo usuário com o código de verificação
        user = User(name=form.name.data, email=form.email.data, password=hashed_password,
                    verification_code=verification_code)
        db.session.add(user)
        db.session.commit()

        # Envia o e-mail de verificação
        send_verification_email(user.email, verification_code)

        flash(f'Um código de verificação foi enviado para {form.email.data}. Por favor, verifique seu e-mail.', 'info')
        return redirect(url_for('auth.verify_email', email=user.email))

    return render_template('register.html', form=form)


@auth.route("/verify_email/<email>", methods=['GET', 'POST'])
def verify_email(email):
    form = VerificationForm()
    user = User.query.filter_by(email=email).first_or_404()

    if form.validate_on_submit():
        if user.verification_code == form.verification_code.data:
            user.email_verified = True  # Marca o e-mail como verificado
            user.verification_code = None  # Remove o código de verificação
            db.session.commit()

            flash('E-mail verificado com sucesso! Agora você pode fazer login.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Código de verificação incorreto. Por favor, tente novamente.', 'danger')

    return render_template('verify_email.html', form=form)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:  # Verifica se o usuário já está logado
        flash('Você já está logado.', 'info')
        return redirect(url_for('main.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)  # Faz o login do usuário

            flash(f'Bem-vindo, {user.name}!', 'success')

            # Verifica se o usuário marcou "Manter-me conectado"
            if form.remember_me.data:
                session.permanent = True  # Sessão permanente
                session.permanent_session_lifetime = timedelta(days=7)  # Sessão dura 7 dias

            return redirect(url_for('main.dashboard'))
        else:
            flash('E-mail ou senha incorretos. Por favor, tente novamente.', 'danger')
    return render_template('login.html', form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()  # Faz o logout do usuário
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('main.home'))

