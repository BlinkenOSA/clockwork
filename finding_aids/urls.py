from django.conf.urls import url

from finding_aids.views import FindingAidsArchivalUnit, \
    FindingAidsInContainerList, FindingAidsInContainerListJson

urlpatterns = [
    # Opening Page
    url(r'^$', FindingAidsArchivalUnit.as_view(), name='choose_archival_unit'),

    # Finding Aids
    url(r'^(?P<container_id>\d+)/$', FindingAidsInContainerList.as_view(), name='finding_aids_container_list'),
    url(r'^datatable/(?P<container_id>\d+)/$', FindingAidsInContainerListJson.as_view(),
        name='finding_aids_container_list_json')


]
