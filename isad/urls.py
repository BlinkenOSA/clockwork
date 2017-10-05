from django.conf.urls import url

from isad.views import IsadList, IsadListJson, IsadCreate, IsadDelete, IsadUpdate, IsadAction

urlpatterns = [
    url(r'^$', IsadList.as_view(), name='list'),

    url(r'^create/(?P<archival_unit>\d+)/$', IsadCreate.as_view(), name='create'),
    url(r'^update/(?P<pk>\d+)/$', IsadUpdate.as_view(), name='update'),
    url(r'^delete/(?P<pk>\d+)/$', IsadDelete.as_view(), name='delete'),

    url(r'^action/(?P<action>\w+)/(?P<pk>\d+)/$', IsadAction.as_view(), name='approval'),

    url(r'^datatable/$', IsadListJson.as_view(), name='isad_list_json'),
]
