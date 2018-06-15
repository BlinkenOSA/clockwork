from __future__ import division

import re
import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Sum
from django.http import JsonResponse
import yaml
import os
from django.views.generic import FormView

from archival_unit.models import ArchivalUnit
from container.models import Container
from dashboard.forms import DashboardArchivalUnitSelectForm
from finding_aids.models import FindingAidsEntity
from isad.models import Isad


class DashboardView(LoginRequiredMixin, FormView):
    template_name = 'dashboard/index.html'
    form_class = DashboardArchivalUnitSelectForm


def infobox(request, module, form_element):
    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, 'static', 'infobox', module + '.yaml')

    for e in ['_from', '_to']:
        form_element = form_element.replace(e, '')

    num_index = re.search(r'\d+', form_element)
    if num_index:
        form_element = form_element[0:num_index.start()-1]

    try:
        with open(file_path, mode='rb') as yamlfile:
            infos = yaml.load(yamlfile)

        if form_element in infos:
            return JsonResponse(infos[form_element])
        else:
            return JsonResponse({'status': 'Form Element Not Found'})
    except IOError:
        return JsonResponse({'status': 'File Not Found'})


def statistics_carrier_types(request, archival_unit):
    data = []
    background_color = []
    labels = []

    containers = get_containers(archival_unit)['containers']
    archival_unit = get_containers(archival_unit)['archival_unit']

    cts = containers.values('carrier_type__type').annotate(total=Count('id')).order_by('-total')

    r = lambda: random.randint(0, 255)
    for ct in cts:
        data.append(ct['total'])
        labels.append(ct['carrier_type__type'])
        background_color.append('rgba(%03d, %03d, %03d, 0.5)' % (r(), r(), r()))

    dataset = {
        'datasets': [{
            'label': 'Containers in %s' % (archival_unit.title_full if archival_unit != '0' else 'every archival unit.'),
            'data': data,
            'backgroundColor': background_color
        }],
        'labels': labels
    }

    return JsonResponse(dataset)


def statistics_linear_meter(request, archival_unit):
    containers = get_containers(archival_unit)['containers']
    archival_unit = get_containers(archival_unit)['archival_unit']

    cw_unit = containers.aggregate(Sum('carrier_type__width'))['carrier_type__width__sum']

    if not cw_unit:
        cw_unit = 0

    if archival_unit == '0':
        cw_top_unit = Container.objects.all().aggregate(Sum('carrier_type__width'))['carrier_type__width__sum']
    else:
        if archival_unit.level == 'F':
            cw_top_unit = Container.objects.filter(archival_unit__fonds=archival_unit.fonds).aggregate(
                Sum('carrier_type__width'))['carrier_type__width__sum']
        elif archival_unit.level == 'SF':
            cw_top_unit = Container.objects.filter(archival_unit__fonds=archival_unit.fonds).aggregate(
                Sum('carrier_type__width'))['carrier_type__width__sum']
        else:
            cw_top_unit = Container.objects.filter(archival_unit__fonds=archival_unit.fonds,
                                                   archival_unit__subfonds=archival_unit.subfonds).aggregate(
                Sum('carrier_type__width'))['carrier_type__width__sum']

    cw_percentage = cw_unit / cw_top_unit * 100

    dataset = {
        'linear_meter': "%.2f m" % (cw_unit / 100),
        'linear_meter_percentage': cw_percentage,
        'linear_meter_message': '%.2f%% of the Fonds' % cw_percentage
    }

    return JsonResponse(dataset)


def statistics_published_items(request, archival_unit):
    containers = get_containers(archival_unit)['containers']
    items = FindingAidsEntity.objects.filter(container__in=containers)

    if items.count() > 0:
        items_all = items.count()
        items_published = items.filter(published=True).count()

        items_percentage = items_published / items_all * 100
    else:
        items_all = 0
        items_published = 0
        items_percentage = 0

    dataset = {
        'published_items': '%d entries' % items_published,
        'published_items_percentage': items_percentage,
        'published_items_message': '%.2f%% of %d' % (items_percentage, items_all)
    }

    return JsonResponse(dataset)


def statistics_isad(request, archival_unit):
    if archival_unit == '0':
        archival_unit_count = ArchivalUnit.objects.count()
        isad_count = Isad.objects.count()
        isad_published = Isad.objects.filter(published=True).count()
    else:
        archival_unit = ArchivalUnit.objects.get(pk=archival_unit)
        if archival_unit.level == 'F':
            isad = Isad.objects.filter(archival_unit__fonds=archival_unit.fonds)
            archival_unit_count = ArchivalUnit.objects.filter(fonds=archival_unit.fonds).count()
            isad_count = isad.count()
            isad_published = isad.filter(published=True).count()
        elif archival_unit.level == 'SF':
            isad = Isad.objects.filter(archival_unit__fonds=archival_unit.fonds,
                                       archival_unit__subfonds=archival_unit.subfonds)
            isad_count = isad.count()
            isad_published = isad.filter(published=True).count()
            archival_unit_count = ArchivalUnit.objects.filter(fonds=archival_unit.fonds,
                                                              subfonds=archival_unit.subfonds).count()
        else:
            isad = Isad.objects.filter(archival_unit__fonds=archival_unit.fonds,
                                             archival_unit__subfonds=archival_unit.subfonds,
                                             archival_unit__series=archival_unit.series)
            isad_count = isad.count()
            isad_published = isad.filter(published=True).count()
            archival_unit_count = ArchivalUnit.objects.filter(fonds=archival_unit.fonds,
                                                              subfonds=archival_unit.subfonds,
                                                              series=archival_unit.series).count()

    isad_percentage = isad_count / archival_unit_count * 100

    dataset = {
        'isad': '%d records' % isad_count,
        'isad_percentage': isad_percentage,
        'isad_message': '%.2f%% of %d (%d published)' % (isad_percentage, archival_unit_count, isad_published)
    }

    return JsonResponse(dataset)


def statistics_duration(request, archival_unit):
    containers = get_containers(archival_unit)['containers']
    items = FindingAidsEntity.objects.filter(container__in=containers)

    duration = items.aggregate(Sum('duration'))['duration__sum']

    if duration:
        hours, remainder = divmod(duration.seconds, 3600)
        hours += duration.days * 24
        minutes, seconds = divmod(remainder, 60)
        duration = '%02d:%02d:%02d' % (hours, minutes, seconds)
    else:
        duration = '00:00:00'

    dataset = {
        'duration': '%s' % str(duration),
        'duration_message': 'in hh:mm:ss'
    }

    return JsonResponse(dataset)


def get_containers(archival_unit):
    if archival_unit == '0':
        containers = Container.objects.all()
    else:
        archival_unit = ArchivalUnit.objects.get(pk=archival_unit)
        if archival_unit.level == 'F':
            containers = Container.objects.filter(archival_unit__fonds=archival_unit.fonds)
        elif archival_unit.level == 'SF':
            containers = Container.objects.filter(archival_unit__fonds=archival_unit.fonds,
                                                  archival_unit__subfonds=archival_unit.subfonds)
        else:
            containers = Container.objects.filter(archival_unit=archival_unit)
    return {'containers': containers, 'archival_unit': archival_unit}
