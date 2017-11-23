# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin


# Register your models here.
from accounts.forms import UserProfileAdminForm
from accounts.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    form = UserProfileAdminForm

admin.site.register(UserProfile, UserProfileAdmin)
