import pysolr
from django.core.management import BaseCommand

from controlled_list.models import PrimaryType
from finding_aids.models import FindingAidsEntity
from finding_aids.tasks import index_add_finding_aids_confidential, index_add_finding_aids


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--type', dest='primary_type', help='Primary Type')

    def handle(self, *args, **options):
        primary_type = PrimaryType.objects.get(type=options['primary_type'])
        finding_aids_entities = FindingAidsEntity.objects.filter(primary_type=primary_type)
        for fa in finding_aids_entities.iterator():
            if fa.published:
                if fa.confidential:
                    index_add_finding_aids_confidential(fa.id)
                else:
                    index_add_finding_aids(fa.id)
                print("Indexed FA Entity: %s" % fa.archival_reference_code)