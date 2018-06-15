from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from isad.models import Isad
from isad.tasks import index_add_isad, index_remove_isad


@receiver(post_save, sender=Isad)
def update_isad_index(sender, **kwargs):
    isad = kwargs["instance"]
    if isad.published:
        index_add_isad.delay(isad_id=isad.id)
    else:
        index_remove_isad.delay(isad_id=isad.id)


@receiver(post_delete, sender=Isad)
def remove_isad_index(sender, **kwargs):
    isad = kwargs["instance"]
    index_remove_isad.delay(isad_id=isad.id)
