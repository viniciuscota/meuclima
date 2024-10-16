from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from datetime import timedelta
from flask_login import LoginManager

bcrypt = Bcrypt()
db = SQLAlchemy()
mail = Mail()  # Inicializando o Mail
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # Configurações de sessão
    app.config['SECRET_KEY'] = 'secret_key_here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meuclima.db'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

    # Configurações do servidor de e-mail (Use suas próprias configurações)
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'meuclima.alerts@gmail.com'
    app.config['MAIL_PASSWORD'] = 'pvqi zluf owvm ilau'
    app.config['MAIL_DEFAULT_SENDER'] = 'meuclima.alerts@gmail.com'

    # Inicialize o LoginManager
    login_manager.init_app(app)

    # Rota de login para redirecionar se o usuário não estiver autenticado
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    bcrypt.init_app(app)
    db.init_app(app)
    mail.init_app(app)

    # Registrando blueprints
    from aplication.auth.routes import auth
    from aplication.main.routes import main
    app.register_blueprint(auth)
    app.register_blueprint(main)

    return app

from aplication.models import User  # Importe o modelo de usuário

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))