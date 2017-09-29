from django.conf.urls import url
from accession.views import AccessionList, AccessionListJson, AccessionCreate, AccessionUpdate, AccessionDelete, \
    AccessionDetail

urlpatterns = [
    url(r'^$', AccessionList.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/$', AccessionDetail.as_view(), name='view'),
    url(r'^create/$', AccessionCreate.as_view(), name='create'),
    url(r'^update/(?P<pk>\d+)/$', AccessionUpdate.as_view(), name='update'),
    url(r'^delete/(?P<pk>\d+)/$', AccessionDelete.as_view(), name='delete'),

    url(r'^datatable/$', AccessionListJson.as_view(), name='list_json'),
]
