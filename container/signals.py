from django.db.models.signals import post_delete
from django.dispatch import receiver

from container.models import Container


@receiver(post_delete, sender=Container)
def update_container_numbers(sender, **kwargs):
    container_no = 1
    containers = Container.objects.filter(archival_unit=kwargs['instance'].archival_unit).order_by('container_no')

    if containers:
        for container in containers:
            container.container_no = container_no
            container_no += 1
            container.save()
