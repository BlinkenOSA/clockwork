from django.conf.urls import url

from isaar.views import IsaarList, IsaarListJson, IsaarCreate, IsaarUpdate, IsaarDetail, IsaarDelete

urlpatterns = [
    url(r'^$', IsaarList.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/$', IsaarDetail.as_view(), name='view'),
    url(r'^create/$', IsaarCreate.as_view(), name='create'),
    url(r'^update/(?P<pk>\d+)/$', IsaarUpdate.as_view(), name='update'),
    url(r'^delete/(?P<pk>\d+)/$', IsaarDelete.as_view(), name='delete'),

    url(r'^datatable/$', IsaarListJson.as_view(), name='isaar_list_json'),
]
