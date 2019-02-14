from flask_mail import Message
from flask import render_template
from . import mail

def mail_message(subject, template,recipients,text_body,html_body):
    email = Message(subject, sender=sender, recipients=recepients)

    email = Message(subject, sender=sender, recipients=recipients)
    email.body = text_body
    email.html = html_body
    mail.send(email)
def reset_email(user):
    token = user.get_reset_password_token()
    email('Reset Password', sender=app.config['MAIL_USERNAME'], recepients=[user.email], text_body=render_template('auth/reset_password.txt', user=user, token=token), html_body=render_template('auth/reset_password.html', user=user, token=token))
