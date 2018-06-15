from __future__ import unicode_literals

from django.apps import AppConfig


class IsadConfig(AppConfig):
    name = 'isad'

    def ready(self):
        super(IsadConfig, self).ready()
        from isad.signals import update_isad_index
        from isad.signals import remove_isad_index