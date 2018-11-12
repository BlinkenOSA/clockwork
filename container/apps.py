from __future__ import unicode_literals

from django.apps import AppConfig


class ContainerConfig(AppConfig):
    name = 'container'

    def ready(self):
        super(ContainerConfig, self).ready()
        from container.signals import update_container_numbers
        from container.signals import update_underlying_finding_aids