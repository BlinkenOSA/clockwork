from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver


class Container(models.Model):
    id = models.AutoField(primary_key=True)

    archival_unit = models.ForeignKey('archival_unit.ArchivalUnit')
    primary_type = models.ForeignKey('controlled_list.PrimaryType')
    carrier_type = models.ForeignKey('controlled_list.CarrierType')

    container_no = models.IntegerField(default=1)
    container_label = models.CharField(max_length=255, blank=True, null=True)

    old_id = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'containers'

    def __unicode__(self):
        return "Container #%s / %s" % (self.container_no, self.carrier_type)


@receiver(post_delete)
def update_container_numbers(sender, **kwargs):
    container_no = 1
    containers = Container.objects.filter(archival_unit=kwargs['instance'].archival_unit).order_by('container_no')
    for container in containers:
        container.container_no = container_no
        container_no += 1
        container.save()
