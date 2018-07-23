from __future__ import unicode_literals
from django.apps import AppConfig


class ArchivalUnitConfig(AppConfig):
    name = 'archival_unit'

    def ready(self):
        super(ArchivalUnitConfig, self).ready()
        from archival_unit.signals import update_isad_title
