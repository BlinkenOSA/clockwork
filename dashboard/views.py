import re
from django.shortcuts import render
from django.http import JsonResponse
import yaml
import os


# Create your views here.
def index(request):
    return render(request, template_name='dashboard/index.html')


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
