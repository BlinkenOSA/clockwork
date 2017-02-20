from django.conf.urls import url

from container.views import ContainerList, ContainerListJson, ContainerCreate, \
    ContainerEditorUpdate

urlpatterns = [
    url(r'^(?P<archival_unit>\d+)/$', ContainerList.as_view(), name='list_with_archival_unit'),

    url(r'^create/$', ContainerCreate.as_view(), name='create'),
    url(r'^editor_update/$', ContainerEditorUpdate.as_view(), name='editor_update'),

    url(r'^datatable/(?P<archival_unit>\d+)/$', ContainerListJson.as_view(), name='container_list_json'),
]
