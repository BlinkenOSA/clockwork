from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from finding_aids.tasks import index_add_finding_aids, index_remove_finding_aids, index_add_finding_aids_confidential

from container.models import Container


@receiver(post_save, sender=Container)
def update_underlying_finding_aids(sender, **kwargs):
    container = kwargs["instance"]
    for finding_aids in container.findingaidsentity_set.iterator():
        if finding_aids.published:
            if finding_aids.confidential:
                index_add_finding_aids_confidential.delay(finding_aids_entity_id=finding_aids.id)
            else:
                index_add_finding_aids.delay(finding_aids_entity_id=finding_aids.id)
        else:
            index_remove_finding_aids.delay(finding_aids_entity_id=finding_aids.id)


@receiver(post_delete, sender=Container)
def update_container_numbers(sender, **kwargs):
    container_no = 1
    containers = Container.objects.filter(archival_unit=kwargs['instance'].archival_unit).order_by('container_no')

    if containers:
        for container in containers:
            container.container_no = container_no
            container_no += 1
            container.save()
