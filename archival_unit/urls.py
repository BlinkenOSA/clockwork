from django.conf.urls import include, url

from archival_unit.views import \
    FondsList, FondsListJson, FondsCreate, FondsUpdate, \
    SubFondsList, SubFondsListJson, SubFondsCreate, SubFondsUpdate, \
    SeriesList, SeriesListJson, SeriesCreate, SeriesUpdate, FondsDelete, SubFondsDelete, SeriesDelete

urlpatterns = [
    url(r'^fonds/$', FondsList.as_view(), name='fonds'),
    url(r'^fonds/datatable/$', FondsListJson.as_view(), name='fonds_list_json'),
    url(r'^fonds/create/$', FondsCreate.as_view(), name='fonds_create'),
    url(r'^fonds/update/(?P<reference_code_id>[-\w]+)/$', FondsUpdate.as_view(), name='fonds_update'),
    url(r'^fonds/delete/(?P<reference_code_id>[-\w]+)/$', FondsDelete.as_view(), name='fonds_delete'),

    url(r'^(?P<parent_reference_code_id>[-\w]+)/subfonds/$', SubFondsList.as_view(), name='subfonds'),
    url(r'^(?P<parent_reference_code_id>[-\w]+)/subfonds/datatable/$', SubFondsListJson.as_view(), name='subfonds_list_json'),
    url(r'^(?P<parent_reference_code_id>[-\w]+)/subfonds/create/$', SubFondsCreate.as_view(), name='subfonds_create'),
    url(r'^subfonds/update/(?P<reference_code_id>[-\w]+)/$', SubFondsUpdate.as_view(), name='subfonds_update'),
    url(r'^subfonds/delete/(?P<reference_code_id>[-\w]+)/$', SubFondsDelete.as_view(), name='subfonds_delete'),

    url(r'^(?P<parent_reference_code_id>[-\w]+)/series/$', SeriesList.as_view(), name='series'),
    url(r'^(?P<parent_reference_code_id>[-\w]+)/series/datatable/$', SeriesListJson.as_view(), name='series_list_json'),
    url(r'^(?P<parent_reference_code_id>[-\w]+)/series/create/$', SeriesCreate.as_view(), name='series_create'),
    url(r'^series/update/(?P<reference_code_id>[-\w]+)/$', SeriesUpdate.as_view(), name='series_update'),
    url(r'^series/delete/(?P<reference_code_id>[-\w]+)/$', SeriesDelete.as_view(), name='series_delete')
]
