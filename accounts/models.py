# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from userena.models import UserenaBaseProfile
from django.contrib.auth.models import User


class UserProfile(UserenaBaseProfile):
    user = models.OneToOneField(User, unique=True, verbose_name='users', related_name='user_profile')