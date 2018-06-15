from __future__ import unicode_literals

from django.apps import AppConfig


class FindingAidsConfig(AppConfig):
    name = 'finding_aids'

    def ready(self):
        super(FindingAidsConfig, self).ready()
        from finding_aids.signals import update_finding_aids_index
