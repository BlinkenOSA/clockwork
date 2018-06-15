from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from finding_aids.models import FindingAidsEntity
from finding_aids.tasks import index_add_finding_aids, index_remove_finding_aids, index_add_finding_aids_confidential


@receiver(post_save, sender=FindingAidsEntity)
def update_finding_aids_index(sender, **kwargs):
    finding_aids = kwargs["instance"]
    if finding_aids.published:
        if finding_aids.confidential:
            index_add_finding_aids_confidential.delay(finding_aids_entity_id=finding_aids.id)
        else:
            index_add_finding_aids.delay(finding_aids_entity_id=finding_aids.id)
    else:
        index_remove_finding_aids.delay(finding_aids_entity_id=finding_aids.id)


@receiver(post_delete, sender=FindingAidsEntity)
def remove_finding_aids_index(sender, **kwargs):
    finding_aids = kwargs["instance"]
    index_remove_finding_aids.delay(finding_aids_entity_id=finding_aids.id)
