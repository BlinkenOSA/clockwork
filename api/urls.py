from django.conf.urls import url

from api.views.catalog.archival_units_detail_view import ArchivalUnitsDetailView
from api.views.catalog.archival_units_tree_quick_view import ArchivalUnitsTreeQuickView
from api.views.catalog.archival_units_tree_view import ArchivalUnitsTreeView
from api.views.catalog.finding_aids_entity_detail_view import FindingAidsEntityDetailView
from api.views.catalog.finding_aids_entity_location_view import FindingAidsEntityLocationView
from api.views.workflow_views import GetSetDigitizedContainer, GetContainerMetadata, FindingAidsEntityListView, \
    FindingAidsEntityUpdateView, GetContainerMetadataByLegacyID, GetFAEntityMetadataByItemID

urlpatterns = [
    url(r'^containers/(?P<barcode>\w+)/$', GetSetDigitizedContainer.as_view(), name='list_set_digitized_container'),
    url(r'^containers/metadata/(?P<barcode>\w+)/$', GetContainerMetadata.as_view(), name='list_get_container_metadata'),
    url(r'^containers/technical_metadata/(?P<barcode>\w+)/$', GetContainerMetadata.as_view(), name='list_get_container_metadata'),

    url(r'^containers/by-legacy-id/(?P<legacy_id>[\w\. -]+)/$', GetContainerMetadataByLegacyID.as_view(), name='get_container_by_legacy_id'),

    url(r'^finding_aids/list/(?P<series_id>\w+)/$', FindingAidsEntityListView.as_view(), name='list_finding_aids_view'),
    url(r'^finding_aids/(?P<pk>\d+)/$', FindingAidsEntityUpdateView.as_view(), name='update_finding_aids_view'),

    url(r'^finding_aids/by-item-id/(?P<item_id>[\w\. -]+)/$', GetFAEntityMetadataByItemID.as_view(), name='get_fa_entity_by_item_id'),

    # Archival Unit Views
    url(r'^catalog/archival-units-tree/(?P<archival_unit_id>[\w\. -]+)/$', ArchivalUnitsTreeView.as_view(),
        name='archival-units-tree'),
    url(r'^catalog/archival-units-tree-quick-view/(?P<archival_unit_id>[\w\. -]+)/$', ArchivalUnitsTreeQuickView.as_view(),
        name='archival-units-tree-quick-view'),
    url(r'^catalog/archival-units/(?P<archival_unit_id>[\w\. -]+)/$', ArchivalUnitsDetailView.as_view(),
        name='archival-units-full-view'),

    # Finding Aids Folder / Item Views
    url(r'^catalog/finding-aids/(?P<fa_entity_catalog_id>[\w\. -]+)/$', FindingAidsEntityDetailView.as_view(),
        name='finding-aids-full-view'),
    url(r'^catalog/finding-aids-location/(?P<fa_entity_catalog_id>[\w\. -]+)/$', FindingAidsEntityLocationView.as_view(),
        name='finding-aids-location-view')
]