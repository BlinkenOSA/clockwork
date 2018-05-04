from django.contrib.auth.models import User
from django.test import TestCase

from accounts.models import UserProfile


class UserProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username='TestUser', email='josh@example.com', password='top_secret')
        self.up = UserProfile.objects.create(user=self.user)

    def test_userprofile_assigned_archival_units(self):
        self.assertEqual(self.up.assigned_archival_units(), 0)

    def test_userprofile_str(self):
        self.assertEqual(str(self.user), 'TestUser')
