import csv
from django.core.management.base import BaseCommand
from store.models import OrderItem


class Command(BaseCommand):
    help = 'Exports all order items to a CSV file with separate quantity column'

    def handle(self, *args, **kwargs):
        file_name = 'orders_export.csv'

        with open(file_name, mode='w', encoding='utf-8-sig', newline='') as file:
            writer = csv.writer(file)

            # Write the header row with separate Quantity column
            writer.writerow(['Order ID', 'Customer', 'Phone', 'City', 'Date',
                            'Product Name', 'Quantity', 'Unit Price', 'Order Total'])

            # Fetch OrderItems instead of Orders directly
            # select_related optimizes DB queries for order and product data
            items = OrderItem.objects.all().select_related('order', 'product')

            for item in items:
                writer.writerow([
                    item.order.id,
                    item.order.full_name,
                    item.order.phone,
                    item.order.city,
                    item.order.created_at.strftime("%Y-%m-%d %H:%M"),
                    item.product.name,     # Product Name
                    item.quantity,         # <--- Quantity in its OWN column
                    item.price,            # Unit Price
                    item.order.total       # Order Total Amount
                ])

        self.stdout.write(self.style.SUCCESS(
            f'Successfully exported {items.count()} items to {file_name}'))
