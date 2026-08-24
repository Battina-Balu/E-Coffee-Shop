import os
from django.core.management.base import BaseCommand
from django.core.management import call_command
from shop.models import Product


class Command(BaseCommand):
    help = "Import coffee data only when the database is empty"

    def handle(self, *args, **options):
        if Product.objects.exists():
            self.stdout.write("Coffee products already exist. Nothing to import.")
            return

        if not os.path.exists("coffee_data.json"):
            self.stdout.write(self.style.ERROR("coffee_data.json not found."))
            return

        call_command("loaddata", "coffee_data.json")
        self.stdout.write(
            self.style.SUCCESS("Coffee data imported successfully.")
        )