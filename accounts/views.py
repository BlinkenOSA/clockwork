import inspect
from itertools import groupby
from operator import itemgetter

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from userena.utils import get_user_profile
from userena.views import profile_edit, profile_detail

from accession.models import Accession
from accounts.forms import UserProfileEditForm
from archival_unit.models import ArchivalUnit
from container.models import Container
from donor.models import Donor
from finding_aids.models import FindingAidsEntity
from isaar.models import Isaar
from isad.models import Isad


def custom_profile_edit(request, username, *args, **kwargs):
    form = UserProfileEditForm
    user = get_object_or_404(get_user_model(), username__iexact=username)
    profile = get_user_profile(user=user)
    extra_context = {'allowed_archival_units': profile.allowed_archival_units.all()}
    return profile_edit(request,
                        edit_profile_form=form,
                        extra_context=extra_context,
                        username=username, *args, **kwargs)


def custom_profile_detail(request, username, *args, **kwargs):
    data = []
    context_data = []

    data += action_by_user(Accession, 'Accession', ['seq', 'title'], username, 'created')
    data += action_by_user(Accession, 'Accession', ['seq', 'title'], username, 'updated')
    data += action_by_user(Donor, 'Donor', ['name'], username, 'created')
    data += action_by_user(Donor, 'Donor', ['name'], username, 'updated')
    data += action_by_user(ArchivalUnit, 'Archival Unit', ['title_full'], username, 'created')
    data += action_by_user(ArchivalUnit, 'Archival Unit', ['title_full'], username, 'updated')
    data += action_by_user(Isaar, 'ISAAR-CPF', ['name'], username, 'created')
    data += action_by_user(Isaar, 'ISAAR-CPF', ['name'], username, 'updated')
    data += action_by_user(Isad, 'ISAD(G)', ['reference_code', 'title'], username, 'created')
    data += action_by_user(Isad, 'ISAD(G)', ['reference_code', 'title'], username, 'updated')
    data += action_by_user(Container, 'Container', ['get_reference_code'], username, 'created')
    data += action_by_user(Container, 'Container', ['get_reference_code'], username, 'updated')
    data += action_by_user(FindingAidsEntity, 'Finding Aids', ['archival_reference_code', 'title', 'template_name'],
                           username, 'created')
    data += action_by_user(FindingAidsEntity, 'Finding Aids', ['archival_reference_code', 'title', 'template_name'],
                           username, 'updated')

    data_array = sorted(data, key=itemgetter('date'), reverse=True)[:20]
    for k, v in groupby(data_array, key=lambda x: x['date']):
        context_data.append({'date': k, 'entries': list(v)})

    return profile_detail(request,
                          username=username,
                          extra_context={'audit_log': context_data},
                          *args, **kwargs)


def action_by_user(model, module, fields, username, cu):
    if cu == 'created':
        qs = model.objects.filter(user_created=username).order_by('-date_created')[:20]
    else:
        qs = model.objects.filter(user_created=username).order_by('-date_updated')[:20]
    return assemble_audit_log(qs, fields, module, cu)


def assemble_audit_log(qs, fields, module, action):
    data = []
    for entry in qs:
        if action == 'created':
            d = entry.date_created
        else:
            d = entry.date_updated

        text_values = map(lambda x: getattr(entry, x)() if inspect.ismethod(getattr(entry, x)) else getattr(entry, x),
                          fields)
        text = " - ".join(filter(None, text_values))

        data.append({
            'module': module,
            'text': text,
            'action': action,
            'date': d.strftime("%Y-%m-%d")
        })
    return data
