from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage, EmailMultiAlternatives


@shared_task
def send_verif_link(message: str, subject: str, email: str):
    """
    Метод создания и отправки сообщения на e-mail
    для подтверждения регистрации
    :return: send_mail
    :rtype: bool
    """
    msg = EmailMessage(
        subject, message, to=[email], from_email=settings.EMAIL_HOST_USER
    )
    msg.content_subtype = 'html'
    try:
        msg.send()  # отправка сообщения на user.email
    except Exception as ex:
        print(ex)
        return False
    return True


@shared_task
def send_link_for_password(subject: str,
                           body: str,
                           from_email: str,
                           to_email: str,
                           html_email: str):
    """
    Метод для создания и отправки сообщения на e-mail адрес
    для смены пароля.
    :return: None
    """
    # Email subject *must not* contain newlines
    email_message = EmailMultiAlternatives(subject,
                                           body,
                                           from_email,
                                           [to_email])
    email_message.attach_alternative(html_email, "text/html")
    email_message.send()  # отправка сообщения
