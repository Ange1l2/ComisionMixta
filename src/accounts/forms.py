from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SelectField, DateField, TelField, SubmitField  # <-- Modificacion de esta Línea
from wtforms.validators import DataRequired, Email, EqualTo, Length
from src.accounts.models import User

import email_validator


class LoginForm(FlaskForm):
    email = EmailField("Correo electrónico", validators=[
                       DataRequired(), Email()])
    password = PasswordField("Contraseña", validators=[DataRequired()])


class RegisterForm(FlaskForm):
    first_name = StringField(
        "Nombre", validators=[DataRequired(), Length(min=2, max=50)]
    )
    last_name = StringField(
        "Apellidos", validators=[DataRequired(), Length(min=2, max=50)]
    )
    birthdate = DateField(
        "Fecha de Nacimiento", format='%Y-%m-%d', validators=[DataRequired()]
    )
    phone = StringField(
        "Teléfono", validators=[DataRequired(), Length(min=10, max=15)]
    )
    user_type = SelectField(
        "Tipo de Usuario",
        choices=[('admin', 'Admin'), ('revisor', 'Revisor'), ('consultor', 'Consultor')],
        validators=[DataRequired()]
    )
    gender = SelectField(
        "Género",
        choices=[('M', 'Masculino'), ('F', 'Femenino')],
        validators=[DataRequired()]
    )
    email = EmailField(
        "Correo electrónico", validators=[DataRequired(), Email(), Length(min=6, max=40)]
    )
    password = PasswordField(
        "Contraseña", validators=[DataRequired(), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        "Repetir contraseña",
        validators=[DataRequired(), EqualTo("password", message="Las contraseñas no coinciden.")],
    )

    def validate(self, extra_validators=None):
        initial_validation = super(RegisterForm, self).validate(extra_validators)
        if not initial_validation:
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append("Este correo ya está registrado")
            return False
        if self.password.data != self.confirm.data:
            self.password.errors.append("La contraseña no coincide")
            return False
        return True


# Agregar esta clase
class ForgotForm(FlaskForm):
    email = EmailField('Correo electrónico', validators=[
                       DataRequired(), Email()])
    submit = SubmitField('Enviar solicitud de cambio de contraseña')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Contraseña', validators=[DataRequired()])
    confirm = PasswordField(
        'Repetir contraseña', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Cambiar contraseña')
