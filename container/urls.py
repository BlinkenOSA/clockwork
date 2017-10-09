from django.conf.urls import url

from container.views import ContainerList, ContainerListJson, ContainerCreate, \
                            ContainerDelete, ContainerUpdate, ContainerAction

urlpatterns = [
    url(r'^(?P<archival_unit>\d+)/$', ContainerList.as_view(), name='list_with_archival_unit'),

    url(r'^create/$', ContainerCreate.as_view(), name='create'),
    url(r'^update/(?P<pk>\d+)/$', ContainerUpdate.as_view(), name='update'),
    url(r'^delete/(?P<pk>\d+)/$', ContainerDelete.as_view(), name='delete'),

    url(r'^action/(?P<action>\w+)/(?P<archival_unit>\d+)/(?P<pk>\w+)/$', ContainerAction.as_view(), name='publish'),

    url(r'^datatable/(?P<archival_unit>\d+)/$', ContainerListJson.as_view(), name='container_list_json'),
]
