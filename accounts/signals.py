from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import UserProfile


@receiver(post_save, sender=User, dispatch_uid='user.created')
def set_user_permissions_upon_create(sender, instance, created, raw, using, **kwargs):
    """ Adds 'change_profile' permission to created user objects """
    if instance.username not in ['AnonymousUser', 'TestUser']:
        if created:
            from guardian.shortcuts import assign_perm
            new_user_profile = UserProfile.objects.create(user=instance)
            new_user_profile.save()
            assign_perm('change_profile', instance, instance.user_profile)
