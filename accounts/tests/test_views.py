from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.urls import reverse

from accession.models import Accession
from accounts.models import UserProfile
from accounts.views import custom_profile_edit, custom_profile_detail, action_by_user


class UserProfileViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username='TestUser',
                                                  email='josh@example.com',
                                                  first_name='Test',
                                                  last_name='User',
                                                  password='top_secret')
        self.up = UserProfile.objects.create(user=self.user)

    def test_custom_profile_edit(self):
        self.factory = RequestFactory()
        request = self.factory.get(reverse('userena_profile_edit', kwargs={'username': 'TestUser'}))
        request.user = self.user
        response = custom_profile_edit(request, self.user.username)
        self.assertEqual(response.context_data['form'].initial['first_name'], 'Test')

    def test_custom_profile_detail(self):
        self.factory = RequestFactory()
        request = self.factory.get(reverse('userena_profile_detail', kwargs={'username': 'TestUser'}))
        request.user = self.user
        response = custom_profile_detail(request, self.user.username)
        self.assertTrue('audit_log' in response.context_data)

    def test_action_by_user_created(self):
        data = action_by_user(Accession, 'Accession', ['seq', 'title'], self.user.username, 'created')
        pass
