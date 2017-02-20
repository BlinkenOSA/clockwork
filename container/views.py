import re
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.generic import FormView, CreateView, View
from django_datatables_view.base_datatable_view import BaseDatatableView

from archival_unit.models import ArchivalUnit
from container.forms import ContainerForm
from container.models import Container
from controlled_list.models import CarrierType, PrimaryType
from finding_aids.models import FindingAidsEntity


class ContainerList(FormView):
    template_name = 'container/list.html'
    form_class = ContainerForm

    def get_context_data(self, **kwargs):
        context = super(ContainerList, self).get_context_data(**kwargs)
        archival_unit = ArchivalUnit.objects.get(pk=self.kwargs['archival_unit'])
        context['archival_unit'] = archival_unit
        archival_unit_names = archival_unit.title_full.split(": ")
        context['fonds_name'] = archival_unit_names[0].replace(archival_unit.reference_code, "").strip()
        context['subfonds_name'] = archival_unit_names[1]
        context['series_name'] = archival_unit_names[2]
        return context


class ContainerListJson(BaseDatatableView):
    model = Container
    columns = ['container_no', 'carrier_type_identifier', 'carrier_type', 'primary_type_identifier', 'primary_type',
               'container_label', 'number_of_fa_entities', 'action']
    order_columns = ['primary_type', 'container_no']
    max_display_length = 500

    def get_initial_queryset(self):
        if self.kwargs['archival_unit'] == '0':
            container = Container.objects.none()
        else:
            archival_unit = ArchivalUnit.objects.get(pk=self.kwargs['archival_unit'])
            container = Container.objects.filter(archival_unit=archival_unit).order_by('container_no')
        return container

    def render_column(self, row, column):
        if column == 'primary_type_identifier':
            return row.primary_type.id
        elif column == 'primary_type':
            return row.primary_type.type
        elif column == 'carrier_type_identifier':
            return row.carrier_type.id
        elif column == 'carrier_type':
            return row.carrier_type.type
        elif column == 'number_of_fa_entities':
            return FindingAidsEntity.objects.filter(container__id=row.id).count()
        elif column == 'action':
            return render_to_string(template_name='container/table_navigate_buttons.html', context={'container': row.id})
        else:
            return super(ContainerListJson, self).render_column(row, column)

    def prepare_results(self, qs):
        json_array = []
        columns = self.get_columns()

        for item in qs:
            data = {"DT_RowId": item.id}
            for column in columns:
                data[column] = self.render_column(item, column)
            json_array.append(data)
        return json_array


class ContainerCreate(CreateView):
    model = Container
    fields = ['archival_unit', 'primary_type', 'carrier_type', 'container_label']

    def form_valid(self, form):
        container = form.instance
        container_number = Container.objects.filter(archival_unit=container.archival_unit).count()
        form.instance.container_no = container_number + 1
        if self.request.is_ajax():
            form.save()
            data = {
                'DT_RowId': container.id,
                'container_no': container.container_no,
                'primary_type': container.primary_type.type,
                'primary_type_identifier': container.primary_type.id,
                'carrier_type': container.carrier_type.type,
                'carrier_type_identifier': container.carrier_type.id,
                'container_label': container.container_label,
                'number_of_fa_entities': 0,
                'action': render_to_string('container/table_navigate_buttons.html', context={'container': container.id})
            }
            return JsonResponse(data)
        else:
            return super(ContainerCreate, self).form_valid(form)


class ContainerEditorUpdate(View):
    def post(self, request):
        request_data = request.POST
        request_type = self.analyze_request(request_data)

        items = self.collect_items(request_data)

        # Move Containers
        if request_type == 'move':
            data = []
            for k, v in request_data.iteritems():
                if k != 'action':
                    id = re.sub("[^0-9]", "", k)
                    container = Container.objects.get(pk=id)
                    container.container_no = v
                    container.save()
                    data.append({
                        "DT_RowId": id,
                        "container_no": container.container_no,
                        "carrier_type_identifier": container.carrier_type.id,
                        "carrier_type": container.carrier_type.type,
                        "primary_type_identifier": container.primary_type.id,
                        "primary_type": container.primary_type.type,
                        "container_label": container.container_label,
                    })

        # Delete Containers
        elif request_type == 'remove':
            for id, item in items.iteritems():
                container = Container.objects.get(pk=id)
                archival_unit = container.archival_unit
                container.delete()
            update_container_numbers(archival_unit)
            data = {'success': 'ok'}

        # Edit Container
        else:
            data = []
            for id, item in items.iteritems():
                container = Container.objects.get(pk=id)

                if item['carrier_type'].isdigit():
                    container.carrier_type = CarrierType.objects.get(pk=item['carrier_type'])

                if item['primary_type'].isdigit():
                    container.primary_type = PrimaryType.objects.get(pk=item['primary_type'])

                container.container_label = item['container_label']
                container.save()
                data.append({
                    "DT_RowId": id,
                    "container_no": container.container_no,
                    "carrier_type_identifier": container.carrier_type.id,
                    "carrier_type": container.carrier_type.type,
                    "primary_type_identifier": container.primary_type.id,
                    "primary_type": container.primary_type.type,
                    "container_label": container.container_label
                })

        return JsonResponse({'data': data})

    @staticmethod
    def analyze_request(request_data):
        request_type = request_data['action']

        if request_type == 'edit':
            request_type = 'move'
            prev_id = ''
            for k, v in request_data.iteritems():
                if k != 'action':
                    id = re.sub("[^0-9]", "", k)
                    if id == prev_id:
                        request_type = 'edit'
                    prev_id = id

        return request_type

    @staticmethod
    def collect_items(data):
        items = {}
        for k, v in data.iteritems():
            if k != 'action':
                id = re.sub("[^0-9]", "", k)
                if id not in items.keys():
                    items[id] = {}
                field = re.sub(r"\bdata\b|[0-9]|\[|\]", "", k)
                items[id][field] = v
        return items


def update_container_numbers(archival_unit):
    container_no = 1
    containers = Container.objects.filter(archival_unit=archival_unit).order_by('container_no')
    for container in containers:
        container.container_no = container_no
        container_no += 1
        container.save()
