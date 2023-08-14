from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        call_command("loaddata", "initial_data.json")  # Имя вашего файла фикстуры
