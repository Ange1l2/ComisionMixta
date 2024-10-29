from threading import Thread
from flask import render_template
from flask_mail import Message
from src import mail, app


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    message = Message(subject, sender=sender, recipients=recipients)
    message.body = text_body
    message.html = html_body
    Thread(target=send_async_email, args=(app, message)).start()


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[CMPAyP UAGro] Solicitud de cambio de contraseña',
               sender=app.config['MAIL_USERNAME'],
               recipients=[user.email],
               text_body=render_template(
                   'accounts/email/reset_password.txt', user=user, token=token),
               html_body=render_template(
                   'accounts/email/reset_password.html', user=user, token=token)
               )
