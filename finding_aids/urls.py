from django.conf.urls import url

from finding_aids.views import FindingAidsArchivalUnit, \
    FindingAidsInContainerList, FindingAidsInContainerListJson, \
    FindingAidsCreate, FindingAidsUpdate, \
    FindingAidsDelete, FindingAidsNewFolderNumber, FindingAidsNewItemNumber, FindingAidsClone

urlpatterns = [
    # Opening Page
    url(r'^$', FindingAidsArchivalUnit.as_view(), name='choose_archival_unit'),

    # Finding Aids
    url(r'^(?P<container_id>\d+)/$', FindingAidsInContainerList.as_view(), name='finding_aids_container_list'),
    url(r'^(?P<container_id>\d+)/create/$', FindingAidsCreate.as_view(), name='create'),
    url(r'^(?P<container_id>\d+)/update/(?P<pk>\d+)$', FindingAidsUpdate.as_view(), name='update'),
    url(r'^(?P<container_id>\d+)/delete/(?P<pk>\d+)$', FindingAidsDelete.as_view(), name='delete'),
    url(r'^(?P<container_id>\d+)/clone/(?P<pk>\d+)$', FindingAidsClone.as_view(), name='clone'),

    url(r'^(?P<container_id>\d+)/get_new_folder/$', FindingAidsNewFolderNumber.as_view(), name='get_new_folder'),
    url(r'^(?P<container_id>\d+)/get_new_item/(?P<folder_no>\d+)$', FindingAidsNewItemNumber.as_view(), name='get_now_folder'),


    url(r'^datatable/(?P<container_id>\d+)/$', FindingAidsInContainerListJson.as_view(),
        name='finding_aids_container_list_json')




]
