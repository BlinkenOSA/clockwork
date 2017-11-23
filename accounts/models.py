# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from userena.models import UserenaBaseProfile
from django.contrib.auth.models import User

from archival_unit.models import ArchivalUnit


class UserProfile(UserenaBaseProfile):
    user = models.OneToOneField(User, unique=True, verbose_name='user', related_name='user_profile')
    allowed_archival_units = models.ManyToManyField(ArchivalUnit, blank=True)

    def assigned_archival_units(self):
        return self.allowed_archival_units.count()

    def __str__(self):
        return self.user.username
