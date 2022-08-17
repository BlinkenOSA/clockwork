from django.conf.urls import url

from api.views import GetSetDigitizedContainer, GetContainerMetadata, FindingAidsEntityListView, \
    FindingAidsEntityUpdateView, GetContainerMetadataByLegacyID, GetFAEntityMetadataByItemID

urlpatterns = [
    url(r'^containers/(?P<barcode>\w+)/$', GetSetDigitizedContainer.as_view(), name='list_set_digitized_container'),
    url(r'^containers/metadata/(?P<barcode>\w+)/$', GetContainerMetadata.as_view(), name='list_get_container_metadata'),
    url(r'^containers/technical_metadata/(?P<barcode>\w+)/$', GetContainerMetadata.as_view(), name='list_get_container_metadata'),

    url(r'^containers/by-legacy-id/(?P<legacy_id>[\w\. -]+)/$', GetContainerMetadataByLegacyID.as_view(), name='get_container_by_legacy_id'),

    url(r'^finding_aids/list/(?P<series_id>\w+)/$', FindingAidsEntityListView.as_view(), name='list_finding_aids_view'),
    url(r'^finding_aids/(?P<pk>\d+)/$', FindingAidsEntityUpdateView.as_view(), name='update_finding_aids_view'),

    url(r'^finding_aids/by-item-id/(?P<item_id>[\w\. -]+)/$', GetFAEntityMetadataByItemID.as_view(), name='get_fa_entity_by_item_id'),

]
