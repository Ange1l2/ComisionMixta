from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, EmailField, TelField, PasswordField, SubmitField  # <-- Modificar esta línea
from wtforms.validators import DataRequired, Email, EqualTo, Length
from src.accounts.models import User

import email_validator


class LoginForm(FlaskForm):
    email = EmailField("Correo electrónico", validators=[DataRequired(), Email()])
    password = PasswordField("Contraseña", validators=[DataRequired()])


class RegisterForm(FlaskForm):
    nombre = StringField(
        "Nombre", validators=[DataRequired(), Length(min=2, max=50)]
    )
    apellidos = StringField(
        "Apellidos", validators=[DataRequired(), Length(min=2, max=100)]    #Capitalice
    )
    fecha_nacimiento = DateField(
        "Fecha de Nacimiento", format='%Y-%m-%d', validators=[DataRequired()]
    )
    genero = SelectField(
        "Género", choices=[('Hombre', 'Hombre'), ('Mujer', 'Mujer'), ('Otro', 'Otro')], validators=[DataRequired()]
    )
    telefono = TelField(
        "Teléfono", validators=[DataRequired(), Length(min=10, max=10)]
    )
    tipo_usuario = SelectField(
        "Tipo de Usuario", choices=[('Normal', 'Normal'), ('Revisor', 'Revisor'), ('Admin', 'Admin')], validators=[DataRequired()]
    )
    email = EmailField(
        "Correo electrónico", validators=[DataRequired(), Email(message=None), Length(min=6, max=40)]
    )
    password = PasswordField(
        "Contraseña", validators=[DataRequired(), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        "Repetir contraseña",
        validators=[
            DataRequired(),
            EqualTo("password", message="Las contraseñas no coinciden."),
        ],
    )

    def validate(self, extra_validators=None):
        initial_validation = super(
            RegisterForm, self).validate(extra_validators)
        if not initial_validation:
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append("Este correo ya está registrado")
            return False
        if self.password.data != self.confirm.data:
            self.password.errors.append("La contraseña NO coincide")
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
