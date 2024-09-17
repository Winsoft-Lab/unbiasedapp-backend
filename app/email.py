# Email settings
# Setting email with threads

from flask import current_app, render_template
from flask_mail import Message
from app import mail


def sendVerificationEmail(email_data):
    app = current_app._get_current_object()

    msg = Message(
        app.config["MAIL_SUBJECT_PREFIX"] + email_data["subject"],
        sender=app.config["MAIL_SENDER"],
        recipients=[email_data["to"]],
    )

    msg.body = render_template(email_data["template"] + ".txt", *email_data)
    msg.html = render_template(
        email_data["template"] + ".html",
        user=email_data["username"],
        token=email_data["token"],
    )

    with app.app_context():
        mail.send(msg)
