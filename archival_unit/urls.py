from django.conf.urls import include, url

from archival_unit.views import \
    FondsList, FondsListJson, FondsCreate, FondsUpdate, \
    SubFondsList, SubFondsListJson, SubFondsCreate, SubFondsUpdate, \
    SeriesList, SeriesListJson, SeriesCreate, SeriesUpdate, FondsDelete, SubFondsDelete, SeriesDelete

urlpatterns = [
    url(r'^fonds/$', FondsList.as_view(), name='fonds'),
    url(r'^fonds/datatable/$', FondsListJson.as_view(), name='fonds_list_json'),
    url(r'^fonds/create/$', FondsCreate.as_view(), name='fonds_create'),
    url(r'^fonds/update/(?P<pk>\d+)/$', FondsUpdate.as_view(), name='fonds_update'),
    url(r'^fonds/delete/(?P<pk>\d+)/$', FondsDelete.as_view(), name='fonds_delete'),

    url(r'^subfonds/(?P<parent_id>\d+)/$', SubFondsList.as_view(), name='subfonds'),
    url(r'^subfonds/(?P<parent_id>\d+)/datatable/$', SubFondsListJson.as_view(), name='subfonds_list_json'),
    url(r'^subfonds/(?P<parent_id>\d+)/create/$', SubFondsCreate.as_view(), name='subfonds_create'),
    url(r'^subfonds/(?P<parent_id>\d+)/update/(?P<pk>\d+)/$', SubFondsUpdate.as_view(), name='subfonds_update'),
    url(r'^subfonds/(?P<parent_id>\d+)/delete/(?P<pk>\d+)/$', SubFondsDelete.as_view(), name='subfonds_delete'),

    url(r'^series/(?P<parent_id>\d+)/$', SeriesList.as_view(), name='series'),
    url(r'^series/(?P<parent_id>\d+)/datatable/$', SeriesListJson.as_view(), name='series_list_json'),
    url(r'^series/(?P<parent_id>\d+)/create/$', SeriesCreate.as_view(), name='series_create'),
    url(r'^series/(?P<parent_id>\d+)/update/(?P<pk>\d+)/$', SeriesUpdate.as_view(), name='series_update'),
    url(r'^series/(?P<parent_id>\d+)/delete/(?P<pk>\d+)/$', SeriesDelete.as_view(), name='series_delete')
]
