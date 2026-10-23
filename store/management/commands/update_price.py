from django.core.management.base import BaseCommand
from store.models import Product
from django.db.models import F


class Command(BaseCommand):
    help = 'Increase all product prices by 10%'

    def handle(self, *args, **kwargs):
        updated_count = Product.objects.all().update(price=F('price') * 1.10)

        self.stdout.write(self.style.SUCCESS(
            f'Successfully updated {updated_count} products.'))
