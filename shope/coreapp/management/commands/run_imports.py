import logging
from typing import List, Tuple
import os

from django.conf import settings
from django.core.mail import send_mail
from django.core.management import BaseCommand
from django.db.utils import IntegrityError

from repositories.profile_repository import ProfileRepository

path_to_dir = os.path.normpath("imports/expected_imports/")
logger = logging.getLogger(__name__)
_profile_repository = ProfileRepository()


def get_paths() -> List[str]:
    """
    Функция для получения файлов, которые нужно проимпортировать
    :return: list[str]
    """
    import_files = list()

    for path in os.listdir(path=path_to_dir):
        abs_path_file = os.path.join(path_to_dir, path)
        if path.endswith((".json", ".xml")):
            import_files.append(abs_path_file)
    return import_files


def apply_imports(import_paths: List[str]) -> Tuple[bool, list, list]:
    """
    Функция для импортирования файлов
    :param import_paths: список файлов для импорта
    :return: bool
    """
    success_path = os.path.normpath(
        "imports/performed_imports/successfully_completed"
    )
    failed_path = os.path.normpath(
        "imports/performed_imports/unsuccessfully_completed"
    )
    files = list()
    errors = list()
    result = True
    for path in import_paths:
        is_error = os.system(f'python manage.py loaddata {path}')
        if not is_error:
            logger.info(f"{os.path.split(path)[1]} - "
                        f"import of this file successfully completed")
            os.rename(path,
                      os.path.join(success_path, os.path.split(path)[1]))
        else:
            logger.error(f"{os.path.split(path)[1]} - "
                         f"failed to import this file")
            errors.append(f"{os.path.split(path)[1]} - "
                          f"failed to import this file")
            os.rename(path,
                      os.path.join(failed_path, os.path.split(path)[1]))
            result = False
        files.append(path)
    return result, files, errors


class Command(BaseCommand):
    """
    Класс для импорта данных в базу данных
    """

    def add_arguments(self, parser):
        parser.add_argument('-p', '--paths', nargs='+',
                            type=str, help='Import paths')
        parser.add_argument('-e', '--email', type=str,
                            help='You email')

    def handle(self, *args, **options):
        if not os.path.exists(os.path.normpath("imports")):
            os.makedirs(os.path.normpath("imports/expected_imports"))
            os.makedirs(os.path.normpath("imports/performed_imports/successfully_completed"))
            os.makedirs(os.path.normpath("imports/performed_imports/unsuccessfully_completed"))
            self.stdout.write(self.style.SUCCESS(
                "The required directories have been successfully created"
            ))
            return
        elif not os.path.exists(os.path.normpath("imports/performed_imports")):
            os.makedirs(os.path.normpath("imports/performed_imports/successfully_completed"))
            os.makedirs(os.path.normpath("imports/performed_imports/unsuccessfully_completed"))
            self.stdout.write(self.style.SUCCESS(
                "The required directories have been successfully created"
            ))
            return
        if options["paths"]:
            paths = [os.path.join(path_to_dir, path)
                     for path in options["paths"]]
        else:
            paths = get_paths()
        result, files, errors = apply_imports(paths)

        if len(files) == 0:
            self.stdout.write(self.style.WARNING(
                "No data was found"
            ))
        elif result:
            self.stdout.write(self.style.SUCCESS(
                "Data import completed successfully"
            ))
        else:
            self.stdout.write(self.style.ERROR(
                "Data import ended with an error"
            ))

        subject = 'Импорт товаров'

        message = """Здравствуйте!\n
Был завершен импорт следующих файлов:\n\n {files}
\nВо время выполнения импорта возникли следующие ошибки:\n\n {errors}
        """.format(
            files='\n'.join(files),
            errors='\n'.join(errors),
        )
        from_email = settings.EMAIL_HOST_USER
        profiles = _profile_repository.get_profile_by_superuser()
        recipient_list = [user.user.email for user in profiles]
        if options["email"]:
            recipient_list.append(options["email"])
        send_mail(subject, message, from_email, recipient_list)
