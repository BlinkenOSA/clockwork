from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand

from accession.models import Accession
from archival_unit.models import ArchivalUnit


class Command(BaseCommand):
    help = 'Creates the default groups and permissions need to run Clockwork AMS.'

    def handle(self, *args, **options):
        grp_accession, c = Group.objects.get_or_create(name='Accessions')
        grp_archival_unit, c = Group.objects.get_or_create(name='Archival Units')
        grp_authority, c = Group.objects.get_or_create(name='Authority Lists')
        grp_controlled_list, c = Group.objects.get_or_create(name='Controlled Lists')
        grp_finding_aids, c = Group.objects.get_or_create(name='Finding Aids')
        grp_isaar, c = Group.objects.get_or_create(name='ISAAR')
        grp_isad, c = Group.objects.get_or_create(name='ISAD(G)')

        ct_accession = ContentType.objects.filter(app_label='accession')
        ct_archival_unit = ContentType.objects.filter(app_label='archival_unit')
        ct_authority = ContentType.objects.filter(app_label='authority')
        ct_container = ContentType.objects.filter(app_label='container')
        ct_controlled_list = ContentType.objects.filter(app_label='controlled_list')
        ct_donor = ContentType.objects.filter(app_label='donor')
        ct_finding_aids = ContentType.objects.filter(app_label='finding_aids')
        ct_isaar = ContentType.objects.filter(app_label='isaar')
        ct_isad = ContentType.objects.filter(app_label='isad')

        # Set Accesson
        for ct in ct_accession:
            self.add_permissions(grp_accession, ct)

        for ct in ct_donor:
            self.add_permissions(grp_accession, ct)

        # Set Archival Unit
        for ct in ct_archival_unit:
            self.add_permissions(grp_archival_unit, ct)

        # Set Authority
        for ct in ct_authority:
            self.add_permissions(grp_authority, ct)

        # Set Controlled List
        for ct in ct_controlled_list:
            self.add_permissions(grp_controlled_list, ct)

        # Set ISAAR
        for ct in ct_isaar:
            self.add_permissions(grp_isaar, ct)

        # Set ISAD(G)
        for ct in ct_isad:
            self.add_permissions(grp_isad, ct)

        # Set Finding Aids
        for ct in ct_finding_aids:
            self.add_permissions(grp_finding_aids, ct)

        for ct in ct_container:
            self.add_permissions(grp_finding_aids, ct)

        for ct in ct_controlled_list:
            if ct.name in ['language usage', 'extent unit', 'corporation role', 'geo role', 'keyword', 'language usage',
                           'person role']:
                self.add_permissions(grp_finding_aids, ct)

        for ct in ct_authority:
            self.add_permissions(grp_finding_aids, ct)

    @staticmethod
    def add_permissions(group, ct):
        perms = Permission.objects.filter(content_type=ct)
        for p in perms:
            group.permissions.add(p)
