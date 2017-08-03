from django.conf.urls import url

from finding_aids.views import FindingAidsArchivalUnit, \
    FindingAidsInContainerList, FindingAidsInContainerListJson, \
    FindingAidsCreate, FindingAidsUpdate, \
    FindingAidsFoldersItemsStatistics

urlpatterns = [
    # Opening Page
    url(r'^$', FindingAidsArchivalUnit.as_view(), name='choose_archival_unit'),

    # Finding Aids
    url(r'^(?P<container_id>\d+)/$', FindingAidsInContainerList.as_view(), name='finding_aids_container_list'),
    url(r'^(?P<container_id>\d+)/create/$', FindingAidsCreate.as_view(), name='create'),
    url(r'^update/(?P<pk>\d+)$', FindingAidsUpdate.as_view(), name='update'),

    url(r'^(?P<container_id>\d+)/statistics/$', FindingAidsFoldersItemsStatistics.as_view(), name='statistics'),

    url(r'^datatable/(?P<container_id>\d+)/$', FindingAidsInContainerListJson.as_view(),
        name='finding_aids_container_list_json')




]
