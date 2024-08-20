from pathlib import Path
import json

from django.core.management import BaseCommand

from catalog.models import Category, Product
from django.conf import settings


class Command(BaseCommand):

    @staticmethod
    def json_read_categories():
        with open(Path(settings.BASE_DIR) / 'catalog.json', encoding="utf-8") as file:
            data = json.load(file)
        return [item for item in data if item['model'] == "catalog.category"]

    @staticmethod
    def json_read_products():
        with open(Path(settings.BASE_DIR) / 'catalog.json', encoding='utf-8') as file:
            data = json.load(file)
        return [item for item in data if item['model'] == 'catalog.product']

    def handle(self, *args, **options):
        Category.objects.all().delete()
        Product.objects.all().delete()

        category_for_create = []
        product_for_create = []

        for category in Command.json_read_categories():
            category_for_create.append(Category(**category['fields']))

        Category.objects.bulk_create(category_for_create)

        for product in Command.json_read_products():
            product_for_create.append(Product(**product['fields']))

        Product.objects.bulk_create(product_for_create)
