from django.conf.urls import url

from mlr.views import *

urlpatterns = [
    url(r'^$', MLRList.as_view(), name='list'),
    url(r'^exportcsv/$', MLRExportCSV.as_view(), name='export_csv'),
    url(r'^update/(?P<pk>\d+)/$', MLRUpdate.as_view(), name='update'),
    url(r'^datatable/$', MLRListJson.as_view(), name='list_json')
]
