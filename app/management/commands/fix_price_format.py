from django.core.management.base import BaseCommand
from django.db.models.functions import Length, Substr
from app.models import Drug, OrderItem


class Command(BaseCommand):
    help = "Strip the trailing '.0' left on prices imported from Excel before the float formatting fix."

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run', action='store_true',
            help='only report how many rows would change',
        )

    def handle(self, *args, **options):
        for model in (Drug, OrderItem):
            qs = model.objects.filter(price__endswith='.0')
            count = qs.count()
            if options['dry_run']:
                self.stdout.write(f'{model.__name__}: {count} rows would be updated')
                continue
            qs.update(price=Substr('price', 1, Length('price') - 2))
            self.stdout.write(self.style.SUCCESS(f'{model.__name__}: {count} rows updated'))
