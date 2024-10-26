from flask import render_template, Blueprint, redirect, url_for, request, flash
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import RegisterForm, LoginForm
from .models import User
from . import db



auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('pages.home'))
    
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Autentificarea a avut succes!')
            return redirect(url_for('pages.home'))

    return render_template('auth/login.html', title='Autentificare', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('pages.home'))
    
    form = RegisterForm()

    if form.validate_on_submit():
        if request.method == 'POST':
            # For password security store the hash in the database
            password_hash = generate_password_hash(form.password.data, 'scrypt')
            user = User(username=form.username.data, email=form.email.data, first_name=form.first_name.data,
                        last_name=form.last_name.data, password=password_hash, college=form.college.data)
            db.session.add(user)
            db.session.commit()
            flash('Inregistrarea a avut succes!')
            return redirect(url_for('pages.home'))

    return render_template('auth/register.html', title='Inregistrare', form=form)


@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
