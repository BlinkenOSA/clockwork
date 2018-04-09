import datetime
from django.test import TestCase

from accession.form import AccessionForm
from authority.models import Country
from donor.models import Donor


class AccessionFormTest(TestCase):
    fixtures = ['accession_copyright_status', 'accession_method', 'country', 'building', 'accession_copyright_status']

    def setUp(self):
        self.donor = Donor.objects.create(
            id=1,
            name='Josh',
            postal_code='1051',
            country=Country.objects.get(country='Hungary'),
            city='Budapest',
            address='Arany Janos u. 32.',
        )

    def test_accession_form_is_valid(self):
        form = AccessionForm(
            data={
                'seq': '2017/1',
                'title': 'Accession #1',
                'method': 1,
                'donor': 1,
                'building': 1,
                'copyright_status': 1,
                'transfer_date': '2018-01-01'
            }
        )
        self.assertTrue(form.is_valid(), form.errors)

    def test_accession_form_is_not_valid(self):
        form = AccessionForm(
            data={
                'seq': '2017/1',
                'title': 'Accession #1',
                'method': 1,
                'donor': 1,
                'building': 1,
                'copyright_status': 1
            }
        )
        self.assertFalse(form.is_valid(), form.errors)