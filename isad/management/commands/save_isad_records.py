from django.core.management import BaseCommand
from isad.models import Isad


class Command(BaseCommand):
    def handle(self, *args, **options):
        for isad in Isad.objects.all():
            isad.save()