from django.core.management import BaseCommand
from django.db.utils import IntegrityError
import os


class Command(BaseCommand):
    """
    Applies all fixtures to the database
    """
    def handle(self, *args, **options):
        self.stdout.write("=" * 40 +
                          "\nApply all fixtures to the database\n\n")
        total_error = list()
        paths = [
            "authapp/fixtures/groups-fixtures.json",
            "authapp/fixtures/users-fixtures.json",
            "profileapp/fixtures/profiles-fixtures.json",
            "productsapp/fixtures/productsapp-fixture.json",
            "productsapp/fixtures/tag_fixtures.json",
            "orderapp/fixtures/orders_fixtures.json",
            "productsapp/fixtures/banners_fixtures.json",
            "productsapp/fixtures/images-fixtures.json",
            "productsapp/fixtures/sliders_fixtures.json",
            "productsapp/fixtures/products-fixture.json",
            "productsapp/fixtures/categories-fixtures.json",
            "productsapp/fixtures/discounts_fixtures.json",
            "coreapp/fixtures/configs.json",
            "productsapp/fixtures/sellers-fixtures.json",
        ]
        for path in paths:
            is_error = os.system(f"python manage.py loaddata {path}")
            if is_error != 0:
                self.stdout.write(self.style.ERROR(
                    f"ERROR! Fixture {path} is not loaded\n"
                ))
                total_error.append(path)
            else:
                self.stdout.write(self.style.SUCCESS(
                    f"Fixture {path} applied successfully\n\n"
                ))
        if not len(total_error):
            self.stdout.write(self.style.SUCCESS(
                "Fixtures applied successfully\n" + "=" * 40))
        else:
            self.stdout.write(self.style.ERROR(
                "When loading fixtures, the following fell off:\n{errors}\n".format(
                    errors='\n'.join(total_error)
                ) + "=" * 40))
