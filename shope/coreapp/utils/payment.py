import requests
import uuid
import os
from coreapp.utils.encode_decode import encode_auth_value


class Payment:
    """
    Сервис работы с платежами через ЮKassa
    """
    _api_url = 'https://api.yookassa.ru/v3/payments/'
    _shop_id = os.getenv("SHOP_ID")
    _api_key = os.getenv("YOOKASSA_API_KEY")
    _auth_data = f'{_shop_id}:{_api_key}'

    @classmethod
    def base_auth_header(cls):
        """
        Формирование заголовка для HTTP Basic Auth
        :return: Словарь с ключом-значением для заголовка Basic Auth
        """
        coded_auth_data = encode_auth_value(cls._auth_data)
        return {'Authorization': f'Basic {coded_auth_data}'}

    @classmethod
    def get_payment_status(cls, payment_id: str):
        """
        Проверка статуса платежа
        :param payment_id: str Идентификатор платежа
        :return: Ответ сервера со статусом платежа
        """
        response = requests.get(url=f'{cls._api_url}{payment_id}',
                                headers=cls.base_auth_header())
        return response

    @classmethod
    def create_payment(cls, amount, order_number, payment_method_id=None,
                       card=None, save_payment_method=False):
        """
        Формирование запроса на создание платежа и его отправка
        :param amount: Сумма платежа
        :param order_number: Номер заказа
        :param payment_method_id: ID сохраненного метода оплаты
        :param card: Реквизиты платежной карты
        :param save_payment_method: Признак для сохранения данных карты
        :return: Ответ сервера с объектом созданного платежа
        """
        headers = cls.base_auth_header()
        headers['Idempotence-Key'] = str(uuid.uuid4())

        # Стандартные поля запроса на создание платежа
        payment_object = {
            'amount': {
                'value': amount,
                'currency': 'RUB'
            },
            'capture': True,
            'description': f'Заказ №{order_number}'
        }

        # Автоплатеж с использованием сохраненного метода оплаты
        if payment_method_id:
            payment_object['payment_method_id'] = payment_method_id
        # Платеж с использованием новой карты
        else:
            payment_object['payment_method_data'] = {
                'type': 'bank_card',
                'card': card
            }
            payment_object['confirmation'] = {
                'type': 'redirect',
                'return_url': ''
            }
            # сохранение карты в качестве платежного метода
            if save_payment_method:
                payment_object['save_payment_method'] = True

        response = requests.post(url=cls._api_url,
                                 headers=headers,
                                 json=payment_object)
        return response
