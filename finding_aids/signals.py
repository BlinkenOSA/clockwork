from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from finding_aids.models import FindingAidsEntity
from finding_aids.tasks import index_add_finding_aids, index_remove_finding_aids, index_add_finding_aids_confidential
from isad.tasks import index_add_isad, index_remove_isad


@receiver(post_save, sender=FindingAidsEntity)
def update_finding_aids_index(sender, **kwargs):
    finding_aids = kwargs["instance"]
    isad = finding_aids.archival_unit.isad
    if finding_aids.published:
        if finding_aids.confidential:
            index_add_finding_aids_confidential.delay(finding_aids_entity_id=finding_aids.id)
        else:
            index_add_finding_aids.delay(finding_aids_entity_id=finding_aids.id)
    else:
        index_remove_finding_aids.delay(finding_aids_entity_id=finding_aids.id)

    if isad.published:
        index_add_isad.delay(isad_id=isad.id)
    else:
        index_remove_isad.delay(isad_id=isad.id)


@receiver(post_delete, sender=FindingAidsEntity)
def remove_finding_aids_index(sender, **kwargs):
    finding_aids = kwargs["instance"]
    isad = finding_aids.archival_unit.isad
    index_remove_finding_aids.delay(finding_aids_entity_id=finding_aids.id)

    if isad.published:
        index_add_isad.delay(isad_id=isad.id)
    else:
        index_remove_isad.delay(isad_id=isad.id)