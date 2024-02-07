from django.core.management.base import BaseCommand
from .factory import create_category, create_product, create_stock


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--cant", nargs="?", default=10)
        parser.add_argument("--c", nargs="?", default=6)

    def handle(self, *args, **options):
        amount = options["cant"]
        category = options["c"]
        if category:
            create_category(amount // 2)
        create_product(amount)
        create_stock(amount)

        self.stdout.write(self.style.SUCCESS("Datos falsos generados correctamente"))
