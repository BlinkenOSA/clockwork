# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        super(AccountsConfig, self).ready()
        from accounts.signals import set_user_permissions_upon_create
