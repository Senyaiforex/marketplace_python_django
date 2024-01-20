from time import sleep

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from PIL import Image
import os


@shared_task
def send_order_confirmation_email(order_id):
    # Получение информации о заказе из базы данных
    # order = Order.objects.get(id=order_id)

    # Отправка письма с подтверждением заказа
    subject = 'Подтверждение заказа'
    message = f'Ваш заказ {order_id} успешно оформлен.'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ['recipient@example.com']
    send_mail(subject, message, from_email, recipient_list)


@shared_task
def process_image(image_path):
    # Открытие изображения с помощью Pillow
    image = Image.open(image_path)

    # Процесс обработки изображения
    # Например, изменение размера, применение фильтров и т.д.
    # image = image.resize((800, 600))
    # image = image.filter(ImageFilter.BLUR)

    # Сохранение обработанного изображения
    processed_image_path = get_processed_image_path(image_path)
    image.save(processed_image_path)

    # Удаление исходного изображения
    os.remove(image_path)

    # Возвращение пути к обработанному изображению
    return processed_image_path


def get_processed_image_path(image_path):
    # Логика формирования пути к обработанному изображению
    # Например, добавление префикса или изменение расширения файла
    processed_image_path = image_path.replace('.jpg', '_processed.jpg')
    return processed_image_path


@shared_task
def import_run():
    """ Функция для фонового импорта файлов """

    while True:
        if os.path.exists((os.path.normpath("imports/expected_imports"))):
            os.system("python manage.py run_imports")
            sleep(10)
        else:
            os.system("python manage.py run_imports")
