import csv
from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from phones.models import Phone


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--path',
            type=str,
            default='phones.csv',
            help='Путь к phones.csv (по умолчанию: phones.csv в корне проекта)',
        )

    def handle(self, *args, **options):

        csv_path = Path(settings.BASE_DIR) / options['path']

        if not csv_path.exists():
            self.stderr.write(self.style.ERROR(f'CSV-файл не найден: {csv_path}'))
            return

        with csv_path.open('r', encoding='utf-8', newline='') as file:
            phones = list(csv.DictReader(file, delimiter=';'))

        created_count = 0
        updated_count = 0

        for row in phones:
            phone_id = int(row['id'])
            name = row['name'].strip()
            image = row['image'].strip()
            price = int(row['price'])
            release_date = datetime.strptime(row['release_date'], '%Y-%m-%d').date()
            lte_exists = row['lte_exists'].strip().lower() in {'true', '1', 'yes', 'y'}

            obj, created = Phone.objects.update_or_create(
                id=phone_id,
                defaults={
                    'name': name,
                    'image': image,
                    'price': price,
                    'release_date': release_date,
                    'lte_exists': lte_exists,
                },
            )

            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Импорт завершён. Добавлено: {created_count}, обновлено: {updated_count}.'
            )
        )