import secrets
import string


def generate_random_string() -> str:
    """
    Метод, который генерирует случайный ключ активации из 13 символов
    return: rand_string
    rtype: string
    """
    letters_and_digits = string.ascii_letters + string.digits
    rand_string = ''.join(secrets.choice(
        letters_and_digits) for i in range(13))
    return rand_string
