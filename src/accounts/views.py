from flask import Blueprint, render_template, flash, redirect, request, url_for
from flask_login import login_user, current_user, logout_user, login_required
from src import bcrypt, db, mail, app
from src.accounts.models import User
from .forms import LoginForm, RegisterForm, ForgotForm, ResetPasswordForm
import sqlalchemy as sqla

from src.accounts.email import send_password_reset_email


accounts_bp = Blueprint('accounts', __name__)


@accounts_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash("Ya has iniciado sesión.", "info")
        return redirect(url_for("home"))
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, request.form["password"]):
            login_user(user)
            return redirect(url_for("core.home"))
        else:
            flash("Correo y/o Contraseña no válida", "danger")
            return render_template("accounts/login.html", form=form)
    return render_template('accounts/login.html', title="Inicio de sesión", form=form)


@accounts_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        flash("Ya estás registrado.", "info")
        return redirect(url_for("core.home"))
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = User(email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash("El usuario ha sido registrado", "success")

        return redirect(url_for("core.home"))

    return render_template("accounts/register.html", title='Registro de usuarios', form=form)


@accounts_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Has cerrado tu sesión", "success")
    return redirect(url_for("accounts.login"))


@ accounts_bp.route("/forgot_password", methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for("accounts.home"))
    form = ForgotForm(request.form)
    if form.validate_on_submit():
        user = db.session.scalar(
            sqla.select(User).where(User.email == form.email.data)
        )
        if user:
            send_password_reset_email(user)
            flash(
                'Revise su correo electrónico y siga las instrucciones para reestablecer su contraseña.')
            return redirect(url_for('accounts.login'))
        flash('El correo proporcionado no está registrado en nuestra base de datos, verifique que esté bien escrito.')
    return render_template("accounts/forgot_password.html", title="Solicitud: Cambio de contraseña", form=form)


@accounts_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('accounts.login'))
    user = User.verify_reset_password_token(token)
    print('User :: ', user)
    if not user:
        return redirect(url_for('accounts.login'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Tu password ha sido cambiado.')
        return redirect(url_for('accounts.login'))
    return render_template('accounts/reset_password.html', form=form)

@accounts_bp.route('/contrato')
def contrato():
    return render_template("accounts/contrato.html", title="Contrato")
