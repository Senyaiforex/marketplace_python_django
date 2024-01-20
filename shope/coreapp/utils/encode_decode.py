import base64


def encode_auth_value(auth_value: str):
    """
    Кодирование значения для заголовка Basic Auth
    :param auth_value: str: значение для кодирования
    :return: str: закодированное значение
    """
    return base64.b64encode(auth_value.encode()).decode()
