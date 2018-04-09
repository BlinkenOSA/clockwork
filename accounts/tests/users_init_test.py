from django.test import TestCase
from userena.models import UserenaSignup


class ModelTests(TestCase):

    def setUp(self):
        # Setup userena permissions
        UserenaSignup.objects.check_permissions()