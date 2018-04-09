import datetime
import json
import urllib

from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.urls import reverse

from accession.models import AccessionMethod, Accession
from accession.views import AccessionListJson, AccessionCreate
from authority.models import Country
from donor.models import Donor


class AccessionModelTest(TestCase):
    fixtures = [
        'accession_copyright_status',
        'accession_method',
        'country',
        'building',
        'accession_copyright_status'
    ]

    def setUp(self):
        self.user = User.objects.create_superuser(username='TestUser', email='josh@example.com', password='top_secret')
        donor = Donor.objects.create(
            id=1,
            name='Josh',
            postal_code='1051',
            country=Country.objects.get(country='Hungary'),
            city='Budapest',
            address='Arany Janos u. 32.',
        )
        accession1 = Accession.objects.create(
            seq=1,
            title='Accession #1',
            transfer_date=datetime.datetime.now(),
            method=AccessionMethod.objects.get(pk=1),
            donor=donor
        )
        accession2 = Accession.objects.create(
            seq=2,
            title='Test',
            transfer_date=datetime.datetime.now(),
            method=AccessionMethod.objects.get(pk=1),
            donor=donor
        )

        self.factory = RequestFactory()

    def test_accession_list_filter_queryset_with_search(self):
        request = self.factory.get(reverse('accession:list_json'), {'search[value]': 'Accession #1'})
        request.user = self.user
        response = AccessionListJson.as_view()(request)
        response_json = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['recordsTotal'], 2)
        self.assertEqual(response_json['recordsFiltered'], 1)

    def test_accession_list_filter_queryset_without_search(self):
        request = self.factory.get(reverse('accession:list_json'))
        request.user = self.user
        response = AccessionListJson.as_view()(request)
        response_json = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['recordsTotal'], 2)

    def test_accession_list_render_column_transfer_date(self):
        request = self.factory.get(reverse('accession:list_json'))
        request.user = self.user
        response = AccessionListJson.as_view()(request)
        response_json = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['data'][0][1], datetime.datetime.now().strftime('%Y-%m-%d'))

    def test_accession_list_render_column_action(self):
        request = self.factory.get(reverse('accession:list_json'))
        request.user = self.user
        response = AccessionListJson.as_view()(request)
        response_json = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['data'][0][3][1:4], 'div')

    def test_accession_create_get_initial(self):
        request = self.factory.get(reverse('accession:create'))
        request.user = self.user
        response = AccessionCreate.as_view()(request)
        self.assertEqual(response.context_data['form'].initial['seq'], '%s/003' % datetime.datetime.now().strftime('%Y'))