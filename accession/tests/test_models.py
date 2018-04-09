import datetime
from django.test import TestCase

from accession.models import AccessionMethod, AccessionCopyrightStatus, Accession
from authority.models import Country
from donor.models import Donor


class AccessionModelTest(TestCase):
    fixtures = ['accession_copyright_status', 'accession_method', 'country']

    def test_accession_str(self):
        dnr = Donor.objects.create(
            name='Josh',
            postal_code='1051',
            country=Country.objects.get(country='Hungary'),
            city='Budapest',
            address='Arany Janos u. 32.'
        )
        ac = Accession.objects.create(
            seq=1,
            title='Accession #1',
            transfer_date=datetime.datetime.now(),
            method=AccessionMethod.objects.get(pk=1),
            donor=dnr
        )
        self.assertEqual(str(ac), '1 - Accession #1')

    def test_accession_method_str(self):
        am = AccessionMethod.objects.get(pk=1)
        self.assertEqual(str(am), 'CEU')

    def test_accession_copyright_status_str(self):
        acs = AccessionCopyrightStatus.objects.get(pk=1)
        self.assertEqual(str(acs), 'Copyright held by Creator')