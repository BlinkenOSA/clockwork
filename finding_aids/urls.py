from django.conf.urls import url

from finding_aids.views.archival_unit_select_views import FindingAidsArchivalUnit
from finding_aids.views.container_list_views import *
from finding_aids.views.finding_aids_entity_views import *
from finding_aids.views.finding_aids_table_view import FindingAidsTableViewList
from finding_aids.views.label_views import FindingAidsLabelDataView
from finding_aids.views.renumber_views import *
from finding_aids.views.template_views import FindingAidsTemplateList, FindingAidsTemplateListJson, \
    FindingAidsTemplateCreate, FindingAidsTemplateUpdate, FindingAidsTemplateDelete

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
    url(r'^(?P<container_id>\d+)/get_new_item/(?P<folder_no>\d+)$', FindingAidsNewItemNumber.as_view(),
        name='get_now_folder'),

    url(r'^(?P<container_id>\d+)/create_template/(?P<template_id>\d+)$', FindingAidsCreateFromTemplate.as_view(),
        name='create_from_template'),

    url(r'^action/(?P<action>\w+)/(?P<container_id>\w+)/(?P<pk>\w+)/$', FindingAidsAction.as_view(), name='publish'),

    url(r'^datatable/(?P<container_id>\d+)/$', FindingAidsInContainerListJson.as_view(),
        name='finding_aids_container_list_json'),

    # Templates
    url(r'^templates/(?P<series_id>\d+)/$', FindingAidsTemplateList.as_view(), name='finding_aids_template_list'),
    url(r'^templates/(?P<series_id>\d+)/create/$', FindingAidsTemplateCreate.as_view(), name='template_create'),
    url(r'^templates/(?P<series_id>\d+)/update/(?P<pk>\d+)$', FindingAidsTemplateUpdate.as_view(),
        name='template_update'),
    url(r'^templates/(?P<series_id>\d+)/delete/(?P<pk>\d+)$', FindingAidsTemplateDelete.as_view(),
        name='template_delete'),

    url(r'^templates/datatable/(?P<series_id>\d+)/$', FindingAidsTemplateListJson.as_view(),
        name='finding_aids_template_list_json'),

    # Table View
    url(r'^table_view/(?P<series_id>\d+)/$', FindingAidsTableViewList.as_view(), name='finding_aids_table_view_list'),

    # Label data
    url(r'^labels/(?P<carrier_type_id>\d+)/(?P<series_id>\d+)/$', FindingAidsLabelDataView.as_view(), name='finding_aids_label_data_view')
]
