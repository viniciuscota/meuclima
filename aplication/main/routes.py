from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from aplication.auth.forms import LoginForm, RegistrationForm, VerificationForm
from aplication.models import User
from aplication import bcrypt, db, mail
from flask_mail import Message
from flask_login import current_user, login_required
import secrets
from datetime import timedelta

main = Blueprint('main', __name__)

@main.route("/")
def home():
    return render_template('home.html')

@main.route("/dashboard")
@login_required
def dashboard():
    if 'user_id' not in session:
        flash('Please log in to access the dashboard.', 'warning')
        return redirect(url_for('auth.login'))
    usuario = current_user.name
    return render_template('dashboard.html', usuario=usuario)

@main.route('/cultivos')
@login_required
def cultivos():
    if 'user_id' not in session:
        flash('Please log in to access the dashboard.', 'warning')
        return redirect(url_for('auth.login'))
    usuario = current_user.name
    return render_template('cultivo.html', usuario=usuario)