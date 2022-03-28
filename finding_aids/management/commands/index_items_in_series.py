import pysolr
from django.core.management import BaseCommand

from archival_unit.models import ArchivalUnit
from finding_aids.models import FindingAidsEntity
from finding_aids.tasks import index_add_finding_aids_confidential, index_add_finding_aids


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--fonds', dest='fonds', help='Fonds Number')
        parser.add_argument('--subfonds', dest='subfonds', help='Subfonds Number')
        parser.add_argument('--series', dest='series', help='Series Number')
        parser.add_argument('--all', dest='all', help='Index everything.')

    def handle(self, *args, **options):
        solr_interface = pysolr.Solr("http://localhost:8983/solr/osacatalog")
        # solr_interface.delete(q='archival_level:Folder/Item', commit=True)

        if options['all']:
            archival_units = ArchivalUnit.objects.filter()
            for archival_unit in archival_units.iterator():
                for fa in FindingAidsEntity.objects.filter(archival_unit=archival_unit).iterator():
                    print("Indexing FA Entity: %s / %s" % (fa.id, fa.archival_reference_code))
                    if fa.published:
                        if fa.confidential:
                            index_add_finding_aids_confidential(fa.id)
                        else:
                            index_add_finding_aids(fa.id)
                        pass
        else:
            archival_unit = ArchivalUnit.objects.get(fonds=options['fonds'],
                                                     subfonds=options['subfonds'],
                                                     series=options['series'])
            finding_aids_entities = FindingAidsEntity.objects.filter(archival_unit=archival_unit)
            for fa in finding_aids_entities.iterator():
                if fa.published:
                    if fa.confidential:
                        index_add_finding_aids_confidential(fa.id)
                    else:
                        index_add_finding_aids(fa.id)
                    print("Indexed FA Entity: %s" % fa.archival_reference_code)