from django.db.models.signals import post_save
from django.dispatch import receiver
from archival_unit.models import ArchivalUnit


@receiver(post_save, sender=ArchivalUnit)
def update_isad_title(sender, instance, **kwargs):
    isad = instance.isad
    if isad:
        isad.title = instance.title
        isad.save()