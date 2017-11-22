from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from userena.utils import get_user_profile
from userena.views import profile_edit
from accounts.forms import UserProfileEditForm


def custom_profile_edit(request, username, *args, **kwargs):
    form = UserProfileEditForm
    user = get_object_or_404(get_user_model(), username__iexact=username)
    profile = get_user_profile(user=user)
    extra_context = {'allowed_archival_units': profile.allowed_archival_units.all()}
    return profile_edit(request,
                        edit_profile_form=form,
                        extra_context=extra_context,
                        username=username, *args, **kwargs)